"""
Delivery tracking repository with CRUD operations.
"""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.delivery_tracking import DeliveryTracking


async def create_delivery_tracking(
    db: AsyncSession,
    data: dict[str, Any],
    user_id: int,
) -> DeliveryTracking:
    """Create a new delivery tracking record."""
    tracking = DeliveryTracking(
        order_id=data["order_id"],
        current_lat=data.get("current_lat"),
        current_lon=data.get("current_lon"),
        estimated_delivery_time=data.get("estimated_delivery_time"),
        delivery_progress=data.get("delivery_progress", 0),
    )
    db.add(tracking)
    await db.commit()
    await db.refresh(tracking)
    return tracking


async def get_delivery_tracking_by_id(
    db: AsyncSession,
    tracking_id: int,
) -> DeliveryTracking | None:
    """Get delivery tracking by ID."""
    return await db.get(DeliveryTracking, tracking_id)


async def get_delivery_trackings_by_order(
    db: AsyncSession,
    order_id: int,
) -> list[DeliveryTracking]:
    """Get all delivery tracking records for an order."""
    result = await db.execute(
        select(DeliveryTracking)
        .where(DeliveryTracking.order_id == order_id)
        .order_by(DeliveryTracking.created_at.desc())
    )
    return list(result.scalars().all())


async def update_delivery_tracking(
    db: AsyncSession,
    tracking_id: int,
    status: str,
    user_id: int,
    location: str | None = None,
    notes: str | None = None,
) -> DeliveryTracking | None:
    """Update delivery tracking status and location."""
    tracking = await get_delivery_tracking_by_id(db, tracking_id)
    if not tracking:
        return None

    # Parse location if provided (format: "lat,lon")
    if location:
        parts = location.split(",")
        if len(parts) == 2:
            try:
                tracking.current_lat = float(parts[0])
                tracking.current_lon = float(parts[1])
            except ValueError:
                pass

    # Map status changes to delivery progress instead of blindly incrementing
    _progress_by_status = {
        "PENDING": 10,
        "ASSIGNED": 30,
        "IN_PROGRESS": 50,
        "COMPLETED": 100,
    }
    tracking.last_updated = datetime.now(UTC)
    tracking.delivery_progress = _progress_by_status.get(status.upper(), tracking.delivery_progress)

    await db.commit()
    await db.refresh(tracking)
    return tracking


async def get_or_create_for_order(db: AsyncSession, order_id: int) -> DeliveryTracking:
    """Get the tracking record for an order, creating it if missing (1:1)."""
    result = await db.execute(select(DeliveryTracking).where(DeliveryTracking.order_id == order_id))
    tracking = result.scalar_one_or_none()
    if tracking:
        return tracking
    tracking = DeliveryTracking(order_id=order_id, delivery_progress=0)
    db.add(tracking)
    await db.commit()
    await db.refresh(tracking)
    return tracking


async def update_location(
    db: AsyncSession,
    tracking: DeliveryTracking,
    lat: float,
    lon: float,
) -> DeliveryTracking:
    """Update courier coordinates."""
    tracking.current_lat = lat
    tracking.current_lon = lon
    tracking.last_updated = datetime.now(UTC)
    await db.commit()
    await db.refresh(tracking)
    return tracking
