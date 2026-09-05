"""
AI endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import require_role
from app.core.database import get_async_session
from app.db.models.user import User

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/predict")
async def predict(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_role(["ADMIN"])),
):
    """AI prediction endpoint (admin only)."""
    # TODO: Implement actual AI prediction logic
    # This is a placeholder for future ML model integration
    return {
        "message": "AI prediction endpoint - to be implemented",
        "status": "placeholder",
        "note": "ML model integration pending",
    }


@router.get("/recommendations")
async def get_recommendations(
    user_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_role(["ADMIN"])),
):
    """Get AI-powered product recommendations."""
    # TODO: Implement recommendation engine
    return {
        "message": "Recommendations endpoint - to be implemented",
        "user_id": user_id,
        "recommendations": [],
    }
