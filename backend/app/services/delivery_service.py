"""
Delivery tracking service layer.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.delivery_tracking import DeliveryTrackingCreate
from app.repositories.delivery_tracking_repo import (
    create_delivery_tracking as create_delivery_tracking_repo,
    get_delivery_tracking_by_id as get_delivery_tracking_repo_by_id,
    get_delivery_trackings_by_order as get_delivery_trackings_repo_by_order,
    update_delivery_tracking as update_delivery_tracking_repo,
)


async def create_delivery_tracking(
    db: AsyncSession,
    data: DeliveryTrackingCreate,
    user_id: int
) -> Optional[dict]:
    """Create new delivery tracking record."""
    return await create_delivery_tracking_repo(db, data, user_id)


async def get_delivery_tracking_by_id(
    db: AsyncSession,
    tracking_id: int
) -> Optional[dict]:
    """Get delivery tracking by ID."""
    return await get_delivery_tracking_repo_by_id(db, tracking_id)


async def get_delivery_trackings_by_order(
    db: AsyncSession,
    order_id: int
) -> list:
    """Get all delivery tracking records for an order."""
    return await get_delivery_trackings_repo_by_order(db, order_id)


async def update_delivery_status(
    db: AsyncSession,
    tracking_id: int,
    status: str,
    user_id: int,
    location: Optional[str] = None,
    notes: Optional[str] = None
) -> Optional[dict]:
    """Update delivery tracking status."""
    return await update_delivery_tracking_repo(
        db, tracking_id, status, user_id, location, notes
    )
