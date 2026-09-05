"""
Delivery tracking service layer.
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.delivery_tracking import DeliveryTracking
from app.repositories.delivery_tracking_repo import (
    create_delivery_tracking as _create_tracking,
)
from app.repositories.delivery_tracking_repo import (
    get_delivery_tracking_by_id as _get_tracking_by_id,
)
from app.repositories.delivery_tracking_repo import (
    get_delivery_trackings_by_order as _get_trackings_by_order,
)
from app.repositories.delivery_tracking_repo import (
    update_delivery_tracking as _update_tracking,
)
from app.schemas.delivery_tracking import (
    DeliveryTrackingCreate,
)


def _tracking_to_schema(tracking: DeliveryTracking | None) -> dict[str, Any] | None:
    """Convert SQLAlchemy model to dict for Pydantic response."""
    if tracking is None:
        return None
    return {
        "id": tracking.id,
        "order_id": tracking.order_id,
        "current_lat": tracking.current_lat,
        "current_lon": tracking.current_lon,
        "last_updated": tracking.last_updated,
        "estimated_delivery_time": tracking.estimated_delivery_time,
        "delivery_progress": tracking.delivery_progress,
        "created_at": tracking.created_at,
        "updated_at": tracking.updated_at,
    }


async def create_delivery_tracking(
    db: AsyncSession,
    data: DeliveryTrackingCreate,
    user_id: int,
) -> dict[str, Any] | None:
    """Create new delivery tracking record."""
    tracking = await _create_tracking(db, data.model_dump(), user_id)
    return _tracking_to_schema(tracking)


async def get_delivery_tracking_by_id(
    db: AsyncSession,
    tracking_id: int,
) -> dict[str, Any] | None:
    """Get delivery tracking by ID."""
    tracking = await _get_tracking_by_id(db, tracking_id)
    return _tracking_to_schema(tracking)


async def get_delivery_trackings_by_order(
    db: AsyncSession,
    order_id: int,
) -> list[dict[str, Any]]:
    """Get all delivery tracking records for an order."""
    trackings = await _get_trackings_by_order(db, order_id)
    return [_tracking_to_schema(t) for t in trackings]


async def update_delivery_status(
    db: AsyncSession,
    tracking_id: int,
    status: str,
    user_id: int,
    location: str | None = None,
    notes: str | None = None,
) -> dict[str, Any] | None:
    """Update delivery tracking status."""
    tracking = await _update_tracking(db, tracking_id, status, user_id, location, notes)
    return _tracking_to_schema(tracking)
