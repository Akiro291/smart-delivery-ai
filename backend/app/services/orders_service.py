"""
Orders service layer.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.order import OrderStatus
from app.db.models.user import UserRole
from app.repositories.order_repo import get_order_by_id, get_order_history
from app.schemas.order import OrderHistoryResponse

# Allowed order status transitions (state machine).
ALLOWED_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.PENDING: {OrderStatus.CONFIRMED, OrderStatus.CANCELLED},
    OrderStatus.CONFIRMED: {OrderStatus.ASSIGNED, OrderStatus.CANCELLED},
    OrderStatus.ASSIGNED: {OrderStatus.IN_PROGRESS, OrderStatus.CANCELLED},
    OrderStatus.IN_PROGRESS: {OrderStatus.COMPLETED, OrderStatus.CANCELLED},
    OrderStatus.COMPLETED: set(),
    OrderStatus.CANCELLED: set(),
}


def is_transition_allowed(old_status: OrderStatus | None, new_status: OrderStatus) -> bool:
    """Check whether a status transition is allowed by the state machine."""
    if old_status is None:
        return True
    return new_status in ALLOWED_TRANSITIONS.get(old_status, set())


def can_view_order(user_role: UserRole, user_id: int, order) -> bool:
    """Access control: admin/manager see all, others only their own orders."""
    if user_role in (UserRole.ADMIN, UserRole.MANAGER):
        return True
    return order.customer_id == user_id or order.courier_id == user_id


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

    if not can_view_order(current_user_role, current_user_id, order):
        return None

    history = await get_order_history(db, order_id)
    return [OrderHistoryResponse.model_validate(h) for h in history]
