"""
Orders service layer.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import UserRole
from app.repositories.order_repo import get_order_by_id, get_order_history
from app.schemas.order import OrderHistoryResponse


async def get_order_history_service(
    db: AsyncSession,
    order_id: int,
    current_user_id: int,
    current_user_role: UserRole,
) -> list[OrderHistoryResponse] | None:
    """Get order history with access control."""
    order = await get_order_by_id(db, order_id)
    if not order:
        return None

    if current_user_role != UserRole.ADMIN and (
        order.customer_id != current_user_id and order.courier_id != current_user_id
    ):
        return None

    history = await get_order_history(db, order_id)
    return [OrderHistoryResponse.model_validate(h) for h in history]
