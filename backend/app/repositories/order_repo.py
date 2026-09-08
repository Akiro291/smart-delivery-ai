"""
Order repository with data access operations.
"""

from decimal import Decimal
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.order import Order, OrderStatus
from app.db.models.order_history import OrderHistory
from app.db.models.order_item import OrderItem


async def get_order_history(db: AsyncSession, order_id: int) -> list[OrderHistory]:
    """Get order history records ordered by creation time."""
    result = await db.execute(
        select(OrderHistory).where(OrderHistory.order_id == order_id).order_by(OrderHistory.created_at.asc())
    )
    return list(result.scalars().all())


async def get_order_by_id(db: AsyncSession, order_id: int) -> Order | None:
    """Get order by ID."""
    return await db.get(Order, order_id)


async def get_orders(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    status: OrderStatus | None = None,
    customer_id: int | None = None,
    courier_id: int | None = None,
) -> list[Order]:
    """Get orders with optional filters."""
    query = select(Order)
    if status:
        query = query.where(Order.status == status)
    if customer_id:
        query = query.where(Order.customer_id == customer_id)
    if courier_id:
        query = query.where(Order.courier_id == courier_id)
    query = query.offset(skip).limit(limit).order_by(Order.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def create_order(db: AsyncSession, order_data: dict[str, Any]) -> Order:
    """Create a new order."""
    order = Order(
        customer_id=order_data["customer_id"],
        from_address=order_data["from_address"],
        to_address=order_data["to_address"],
        total_amount=Decimal(str(order_data["total_amount"])),
        description=order_data.get("description"),
        is_priority=int(order_data.get("is_priority", 0)),
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def update_order_status(
    db: AsyncSession,
    order_id: int,
    new_status: OrderStatus,
    courier_id: int | None = None,
    notes: str | None = None,
    changed_by: int | None = None,
) -> Order | None:
    """Update order status and create history record.

    Returns None if the order does not exist or the transition is not allowed.
    """
    order = await get_order_by_id(db, order_id)
    if not order:
        return None

    from app.services.orders_service import is_transition_allowed

    if not is_transition_allowed(order.status, new_status):
        return None

    old_status = order.status
    order.status = new_status
    if courier_id is not None:
        order.courier_id = courier_id

    # Create history record
    history = OrderHistory(
        order_id=order_id,
        from_status=old_status.value if old_status else None,
        to_status=new_status.value,
        changed_by=changed_by,
        notes=notes,
    )
    db.add(history)

    await db.commit()
    await db.refresh(order)
    return order


async def assign_courier(
    db: AsyncSession,
    order: Order,
    courier_id: int,
    assigned_by: int | None = None,
) -> Order:
    """Assign a courier to an order and move it to ASSIGNED (with history)."""
    old_status = order.status
    order.courier_id = courier_id
    if order.status in (OrderStatus.PENDING, OrderStatus.CONFIRMED):
        order.status = OrderStatus.ASSIGNED
    db.add(
        OrderHistory(
            order_id=order.id,
            from_status=old_status,
            to_status=order.status,
            changed_by=assigned_by,
            notes=f"Courier {courier_id} assigned",
        )
    )
    await db.commit()
    await db.refresh(order)
    return order


async def get_order_stats(db: AsyncSession) -> dict[str, Any]:
    """Aggregate order statistics for dashboards."""
    result = await db.execute(select(Order.status, func.count(Order.id)).group_by(Order.status))
    counts = {row[0].value: row[1] for row in result.all()}

    total = sum(counts.values())
    revenue_result = await db.execute(
        select(func.coalesce(func.sum(Order.total_amount), 0)).where(Order.status == OrderStatus.COMPLETED)
    )
    revenue = revenue_result.scalar_one()

    return {
        "total": total,
        "by_status": counts,
        "completed_revenue": float(revenue),
        "active": total - counts.get(OrderStatus.COMPLETED.value, 0) - counts.get(OrderStatus.CANCELLED.value, 0),
    }


async def update_order(
    db: AsyncSession,
    order: Order,
    order_data: dict[str, Any],
) -> Order:
    """Update order fields and record a history entry when the status changes."""
    old_status = order.status
    for field, value in order_data.items():
        if value is None or not hasattr(order, field):
            continue
        if field == "status" and not isinstance(value, OrderStatus):
            setattr(order, field, OrderStatus(value))
        else:
            setattr(order, field, value)
    if order.status != old_status:
        db.add(
            OrderHistory(
                order_id=order.id,
                from_status=old_status,
                to_status=order.status,
                notes="Updated via API",
            )
        )
    await db.commit()
    await db.refresh(order)
    return order


async def create_order_items(
    db: AsyncSession,
    order_id: int,
    items_data: list[dict[str, Any]],
) -> list[OrderItem]:
    """Create order items for an order."""
    order_items = []
    for item_data in items_data:
        order_item = OrderItem(
            order_id=order_id,
            product_id=item_data["product_id"],
            product_name=item_data["product_name"],
            quantity=item_data["quantity"],
            price=item_data["price"],
        )
        db.add(order_item)
        order_items.append(order_item)

    await db.commit()
    for item in order_items:
        await db.refresh(item)
    return order_items


async def get_order_items(db: AsyncSession, order_id: int) -> list[OrderItem]:
    """Get all items for an order."""
    result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order_id).order_by(OrderItem.created_at.asc())
    )
    return list(result.scalars().all())
