"""
Delivery tracking endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user, require_role
from app.core.database import get_async_session
from app.db.models.user import User, UserRole
from app.repositories.delivery_tracking_repo import (
    get_or_create_for_order,
    update_location,
)
from app.repositories.order_repo import get_order_by_id
from app.schemas.delivery_tracking import DeliveryTracking, DeliveryTrackingCreate
from app.services.delivery_service import (
    create_delivery_tracking,
    get_delivery_tracking_by_id,
    get_delivery_trackings_by_order,
    update_delivery_status,
)

router = APIRouter(prefix="/delivery", tags=["delivery"])


class UpdateStatusRequest(BaseModel):
    new_status: str
    location: str | None = None
    notes: str | None = None


def _ensure_order_access(current_user: User, order) -> None:
    """Raise 403 unless the user is admin, the order owner or the assigned courier."""
    if current_user.role == UserRole.ADMIN:
        return
    if order.customer_id == current_user.id or order.courier_id == current_user.id:
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied",
    )


@router.post("/", response_model=DeliveryTracking, status_code=201)
async def create_delivery(
    data: DeliveryTrackingCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_role(["ADMIN", "COURIER"])),
):
    """Create new delivery tracking record (admin or courier only)."""
    order = await get_order_by_id(db, data.order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    tracking = await create_delivery_tracking(db, data, current_user.id)
    if not tracking:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating delivery tracking",
        )
    return tracking


@router.get("/{tracking_id}", response_model=DeliveryTracking)
async def get_delivery(
    tracking_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Get delivery tracking by ID."""
    tracking = await get_delivery_tracking_by_id(db, tracking_id)
    if not tracking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery tracking not found",
        )
    order = await get_order_by_id(db, tracking.order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    _ensure_order_access(current_user, order)
    return tracking


@router.get("/order/{order_id}", response_model=list[DeliveryTracking])
async def get_delivery_by_order(
    order_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Get all delivery tracking records for an order."""
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    _ensure_order_access(current_user, order)
    trackings = await get_delivery_trackings_by_order(db, order_id)
    return trackings


@router.put("/{tracking_id}/status", response_model=DeliveryTracking)
async def update_delivery_status_endpoint(
    tracking_id: int,
    body: UpdateStatusRequest,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_role(["ADMIN", "COURIER"])),
):
    """Update delivery tracking status. Only admin or courier can update."""
    tracking = await update_delivery_status(
        db, tracking_id, body.new_status, current_user.id, body.location, body.notes
    )
    if not tracking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery tracking not found",
        )
    await _publish_tracking_event(db, tracking)
    return tracking


class LocationUpdateRequest(BaseModel):
    lat: float
    lon: float


@router.put("/order/{order_id}/location", response_model=DeliveryTracking)
async def update_order_location(
    order_id: int,
    body: LocationUpdateRequest,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_role(["ADMIN", "COURIER"])),
):
    """Courier sends current coordinates; tracking is updated and broadcast."""
    if not -90 <= body.lat <= 90 or not -180 <= body.lon <= 180:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid coordinates")
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if current_user.role == UserRole.COURIER and order.courier_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    tracking = await get_or_create_for_order(db, order_id)
    tracking = await update_location(db, tracking, body.lat, body.lon)
    await _publish_tracking_event(db, tracking)
    return tracking


async def _publish_tracking_event(db: AsyncSession, tracking) -> None:
    """Broadcast a tracking update to interested users."""
    from app.core.redis import publish_ws_event

    order = await get_order_by_id(db, tracking.order_id)
    audience: list[int] | None = None
    if order:
        audience = [order.customer_id]
        if order.courier_id:
            audience.append(order.courier_id)
    await publish_ws_event(
        "tracking.updated",
        {
            "order_id": tracking.order_id,
            "lat": tracking.current_lat,
            "lon": tracking.current_lon,
            "progress": tracking.delivery_progress,
            "estimated_delivery_time": tracking.estimated_delivery_time,
        },
        user_ids=audience,
    )
