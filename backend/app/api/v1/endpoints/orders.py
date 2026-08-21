"""
Orders endpoints.
"""

from typing import List, cast

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.db.models.user import User, UserRole
from app.repositories.order_repo import get_order_by_id
from app.services.orders_service import get_order_history_service
from app.schemas.order import OrderHistoryResponse
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/")
async def list_orders():
    return {"message": "Orders list endpoint - to be implemented"}


@router.get("/{order_id}")
async def get_order(order_id: int):
    return {"message": f"Order {order_id} endpoint - to be implemented"}


@router.get("/{order_id}/history", response_model=List[OrderHistoryResponse])
async def get_order_history_endpoint(
    order_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Get order history timeline."""
    history = await get_order_history_service(
        db=db,
        order_id=order_id,
        current_user_id=current_user.id,
        current_user_role=cast(UserRole, current_user.role),
    )
    if history is None:
        order = await get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return history
