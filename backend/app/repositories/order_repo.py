"""
Order repository with data access operations.
"""

from decimal import Decimal
from typing import Any

from sqlalchemy import select
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
) -> Order | None:
    """Update order status and create history record."""
    order = await get_order_by_id(db, order_id)
    if not order:
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
        notes=notes,
    )
    db.add(history)

    await db.commit()
    await db.refresh(order)
    return order


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
