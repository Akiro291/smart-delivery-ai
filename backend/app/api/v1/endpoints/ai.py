"""
AI endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user, require_role
from app.core.database import get_async_session
from app.db.models.user import User
from app.repositories.order_repo import get_order_by_id
from app.services.ai_service import get_ai_service

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/predict")
async def predict(
    order_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_role(["ADMIN", "MANAGER"])),
):
    """Predict delivery time for an order (admin/manager)."""
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    service = get_ai_service()
    return await service.predict_delivery_time(db, order)


@router.get("/recommendations")
async def get_recommendations(
    user_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_role(["ADMIN", "MANAGER"])),
):
    """Get AI-powered product recommendations (placeholder)."""
    return {
        "message": "Recommendations endpoint - to be implemented",
        "user_id": user_id,
        "recommendations": [],
    }


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
async def chat(
    body: ChatRequest,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """AI assistant chat (any authenticated user)."""
    if not body.message.strip():
        raise HTTPException(status_code=400, detail="Message is empty")
    service = get_ai_service()
    return await service.chat(db, current_user, body.message.strip()[:2000])
