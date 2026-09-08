"""
Orders endpoints.
"""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user, require_role
from app.core.database import get_async_session
from app.db.models.order import OrderStatus
from app.db.models.user import User, UserRole
from app.repositories.order_repo import (
    assign_courier,
    get_order_by_id,
    get_order_stats,
    get_orders,
)
from app.repositories.user_repo import get_user_by_id
from app.schemas.order import Order, OrderCreate, OrderHistoryResponse, OrderUpdate
from app.schemas.stats import OrderStatsResponse
from app.services.orders_service import (
    can_view_order,
    get_order_history_service,
    is_transition_allowed,
)

router = APIRouter(prefix="/orders", tags=["orders"])

# Roles that manage orders (back office)
MANAGER_ROLES = [UserRole.ADMIN.name, UserRole.MANAGER.name]


@router.get("/", response_model=list[Order])
async def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    status_filter: str | None = Query(None),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Get orders list with filtering."""
    if current_user.role in (UserRole.ADMIN, UserRole.MANAGER):
        # Admin/manager see all orders
        order_status = OrderStatus(status_filter) if status_filter else None
        orders = await get_orders(db, skip, limit, order_status)
    elif current_user.role == UserRole.COURIER:
        orders = await get_orders(db, skip, limit, courier_id=current_user.id)
    else:
        orders = await get_orders(db, skip, limit, customer_id=current_user.id)
    return orders


@router.get("/stats/summary", response_model=OrderStatsResponse)
async def get_stats(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_role(MANAGER_ROLES)),
):
    """Aggregate order statistics for dashboards (admin/manager only)."""
    return await get_order_stats(db)


class AssignCourierRequest(BaseModel):
    courier_id: int


@router.post("/{order_id}/assign", response_model=Order)
async def assign_courier_endpoint(
    order_id: int,
    body: AssignCourierRequest,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_role(MANAGER_ROLES)),
):
    """Assign a courier to an order (admin/manager only)."""
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if order.status == OrderStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot assign courier to a cancelled order"
        )
    courier = await get_user_by_id(db, body.courier_id)
    if not courier or courier.role != UserRole.COURIER:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a courier")
    if not courier.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Courier is inactive")
    updated = await assign_courier(db, order, body.courier_id, assigned_by=current_user.id)
    await _publish_order_event(db, updated, "order.assigned")
    await _notify_status(db, updated, current_user)
    return updated


async def _notify_status(db: AsyncSession, order, actor: User | None) -> None:
    """Dispatch status-change notifications (in-app + external, best-effort)."""
    from app.services.notification_events import notify_order_status_change

    try:
        await notify_order_status_change(db, order, order.status.value, actor)
    except Exception:  # pragma: no cover - notification failure must not fail request
        pass


async def _publish_order_event(db: AsyncSession, order, event_type: str) -> None:
    """Broadcast an order event to customer and assigned courier."""
    from app.core.redis import publish_ws_event

    audience = [order.customer_id]
    if order.courier_id:
        audience.append(order.courier_id)
    await publish_ws_event(
        event_type,
        {"order_id": order.id, "status": order.status.value, "courier_id": order.courier_id},
        user_ids=audience,
    )


@router.get("/{order_id}", response_model=Order)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Get order by ID."""
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    # Access control: admin/manager see all, others only their own orders
    if not can_view_order(current_user.role, current_user.id, order):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return order


@router.get("/{order_id}/history", response_model=list[OrderHistoryResponse])
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
        current_user_role=current_user.role,
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


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Create a new order."""
    from app.repositories.order_repo import create_order as create_order_repo
    from app.repositories.order_repo import create_order_items

    # Never trust the client with the total when line items are provided
    if order_data.items:
        order_total = sum(
            (Decimal(str(item.price)) * item.quantity for item in order_data.items),
            Decimal("0"),
        )
    else:
        order_total = order_data.total_amount

    order = await create_order_repo(
        db,
        {
            "customer_id": current_user.id,
            "from_address": order_data.from_address,
            "to_address": order_data.to_address,
            "total_amount": order_total,
            "description": order_data.description,
            "is_priority": order_data.is_priority,
        },
    )

    if order_data.items:
        await create_order_items(db, order.id, [item.model_dump() for item in order_data.items])

    return order


@router.put("/{order_id}", response_model=Order)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Update an order."""
    from app.repositories.order_repo import update_order as update_order_repo

    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    # Admin/manager can update any order, customers only their own;
    # the assigned courier may change the status of their order.
    is_manager = current_user.role in (UserRole.ADMIN, UserRole.MANAGER)
    is_assigned_courier = current_user.role == UserRole.COURIER and order.courier_id == current_user.id
    if not is_manager and not is_assigned_courier and order.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    update_data = order_data.model_dump(exclude_unset=True)
    if not is_manager:
        # Couriers may only move the status forward; customers cannot touch status/courier
        if is_assigned_courier:
            update_data.pop("courier_id", None)
            update_data = {"status": update_data["status"]} if "status" in update_data else {}
        else:
            update_data.pop("status", None)
            update_data.pop("courier_id", None)

    # Enforce the status state machine
    if "status" in update_data and update_data["status"] is not None:
        new_status = OrderStatus(update_data["status"])
        if not is_transition_allowed(order.status, new_status):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status transition from {order.status.value} to {new_status.value}",
            )

    updated = await update_order_repo(db, order, update_data)
    if "status" in update_data and update_data.get("status") is not None:
        await _publish_order_event(db, updated, "order.status_changed")
        await _notify_status(db, updated, current_user)
    return updated
