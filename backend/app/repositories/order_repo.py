"""
Order repository with data access operations.
"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.order_history import OrderHistory
from app.db.models.order import Order


async def get_order_history(db: AsyncSession, order_id: int) -> List[OrderHistory]:
    """Get order history records ordered by creation time."""
    result = await db.execute(
        select(OrderHistory)
        .where(OrderHistory.order_id == order_id)
        .order_by(OrderHistory.created_at.asc())
    )
    return list(result.scalars().all())


async def get_order_by_id(db: AsyncSession, order_id: int) -> Optional[Order]:
    """Get order by ID."""
    return await db.get(Order, order_id)
