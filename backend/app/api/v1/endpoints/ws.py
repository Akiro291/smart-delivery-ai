"""
WebSocket endpoint with JWT auth and Redis pub/sub fanout.
"""

import asyncio

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect, status

from app.api.v1.dependencies import decode_token
from app.core.logging import get_logger
from app.core.redis import subscribe_ws_events
from app.db.models.user import User, UserRole
from app.repositories.user_repo import get_user_by_id

logger = get_logger(__name__)

router = APIRouter()

# Connected users: user_id -> {websocket: user_role}
_connections: dict[int, dict[WebSocket, UserRole]] = {}


def _can_see_event(user_role: UserRole, user_id: int, event: dict) -> bool:
    """Filter events by audience."""
    target_ids = event.get("user_ids")
    if not target_ids:
        return True
    if user_id in target_ids:
        return True
    return user_role in (UserRole.ADMIN, UserRole.MANAGER)


async def _event_broadcaster() -> None:
    """Background task: read Redis pub/sub and push to local connections."""
    async for event in subscribe_ws_events():
        for user_id, sockets in list(_connections.items()):
            for ws, role in list(sockets.items()):
                try:
                    if _can_see_event(role, user_id, event):
                        await ws.send_json(event)
                except Exception:  # pragma: no cover - connection failure path
                    sockets.pop(ws, None)
            if not sockets:
                _connections.pop(user_id, None)


_broadcaster_task: asyncio.Task | None = None


def _ensure_broadcaster() -> None:
    global _broadcaster_task
    if _broadcaster_task is None or _broadcaster_task.done():
        _broadcaster_task = asyncio.create_task(_event_broadcaster())


async def _authenticate(token: str) -> User | None:
    """Resolve and validate a user from an access token."""
    payload = decode_token(token)
    if not payload or payload.get("type") == "refresh":
        return None
    raw_user_id = payload.get("sub")
    if not raw_user_id:
        return None
    from app.core.database import async_session_factory

    async with async_session_factory() as session:
        user = await get_user_by_id(session, user_id=int(raw_user_id))
    if not user or not user.is_active:
        return None
    return user


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    """WebSocket connection endpoint. JWT (access token) passed via query param.

    Note: token-in-query is acceptable for dev; in production prefer
    Sec-WebSocket-Protocol or short-lived one-time tickets.
    """
    user = await _authenticate(token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    _ensure_broadcaster()
    await websocket.accept()
    _connections.setdefault(user.id, {})[websocket] = user.role
    try:
        # Keep the connection alive; client messages are ignored for now
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        sockets = _connections.get(user.id)
        if sockets:
            sockets.pop(websocket, None)
            if not sockets:
                _connections.pop(user.id, None)
