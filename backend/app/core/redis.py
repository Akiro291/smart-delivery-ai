"""
Redis helpers: connection, rate limiting buckets, pub/sub fanout for WebSocket.
"""

import json

from redis import asyncio as aioredis

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_redis: aioredis.Redis | None = None


def get_redis() -> aioredis.Redis:
    """Get (and lazily create) the shared async Redis client."""
    global _redis
    if _redis is None:
        password = settings.REDIS_PASSWORD or None
        _redis = aioredis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=password,
            decode_responses=True,
        )
    return _redis


async def close_redis() -> None:
    """Close the shared Redis client."""
    global _redis
    if _redis is not None:
        await _redis.aclose()
        _redis = None


async def ping_redis() -> bool:
    """Check Redis connectivity. Returns False instead of raising."""
    try:
        await get_redis().ping()
        return True
    except Exception as exc:  # pragma: no cover - network failure path
        logger.warning(f"Redis ping failed: {exc}")
        return False


# ---------------------------------------------------------------------------
# Rate limiting (fixed-window counter, best-effort: allows on Redis failure)
# ---------------------------------------------------------------------------


async def rate_limit_hit(key: str, limit: int, window_seconds: int) -> bool:
    """Record a hit for `key` and return True if the limit is exceeded."""
    try:
        r = get_redis()
        bucket_key = f"ratelimit:{key}"
        async with r.pipeline(transaction=True) as pipe:
            pipe.incr(bucket_key)
            pipe.expire(bucket_key, window_seconds, nx=True)
            results = await pipe.execute()
        return int(results[0]) > limit
    except Exception as exc:  # pragma: no cover - network failure path
        logger.warning(f"Rate limit check failed (allowing request): {exc}")
        return False


# ---------------------------------------------------------------------------
# WebSocket event fanout via pub/sub
# ---------------------------------------------------------------------------

WS_CHANNEL = "ws:events"


async def publish_ws_event(event_type: str, payload: dict, user_ids: list[int] | None = None) -> None:
    """Publish a WebSocket event; fanout is handled by ws listeners.

    `user_ids` limits the audience; None means broadcast to all connected users.
    """
    message = json.dumps({"type": event_type, "payload": payload, "user_ids": user_ids})
    try:
        await get_redis().publish(WS_CHANNEL, message)
    except Exception as exc:  # pragma: no cover - network failure path
        logger.warning(f"Failed to publish ws event: {exc}")


async def subscribe_ws_events():
    """Subscribe to the WebSocket event channel and yield parsed messages."""
    r = get_redis()
    pubsub = r.pubsub()
    await pubsub.subscribe(WS_CHANNEL)
    try:
        async for message in pubsub.listen():
            if message.get("type") != "message":
                continue
            try:
                yield json.loads(message["data"])
            except (json.JSONDecodeError, TypeError):
                continue
    finally:
        await pubsub.aclose()


# ---------------------------------------------------------------------------
# Password reset tokens
# ---------------------------------------------------------------------------

RESET_TOKEN_TTL = 3600  # 1 hour


def _reset_token_key(token: str) -> str:
    return f"pwd_reset:{token}"


async def store_reset_token(token: str, user_id: int) -> None:
    await get_redis().set(_reset_token_key(token), str(user_id), ex=RESET_TOKEN_TTL)


async def consume_reset_token(token: str) -> int | None:
    """Validate a reset token and delete it (single use). Returns user_id or None."""
    key = _reset_token_key(token)
    user_id = await get_redis().get(key)
    if user_id is None:
        return None
    await get_redis().delete(key)
    return int(user_id)
