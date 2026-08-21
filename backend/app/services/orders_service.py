"""
Orders service layer.
"""

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import UserRole
from app.repositories.order_repo import get_order_history, get_order_by_id
from app.schemas.order import OrderHistoryResponse


async def get_order_history_service(
    db: AsyncSession,
    order_id: int,
    current_user_id: int,
    current_user_role: UserRole,
) -> Optional[List[OrderHistoryResponse]]:
    """Get order history with access control."""
    order = await get_order_by_id(db, order_id)
    if not order:
        return None

    if current_user_role not in (UserRole.ADMIN, UserRole.MANAGER):
        if order.customer_id != current_user_id and order.courier_id != current_user_id:
            return []

    history = await get_order_history(db, order_id)
    return [OrderHistoryResponse.model_validate(h) for h in history]
