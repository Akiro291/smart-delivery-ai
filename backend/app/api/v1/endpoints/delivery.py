"""
Delivery tracking endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.schemas.delivery_tracking import DeliveryTrackingCreate, DeliveryTracking
from app.services.delivery_service import (
    create_delivery_tracking,
    get_delivery_tracking_by_id,
    get_delivery_trackings_by_order,
    update_delivery_status,
)
from app.repositories.delivery_tracking_repo import get_delivery_tracking_repo
from app.api.v1.dependencies import get_current_user
from app.db.models.user import User

router = APIRouter(prefix="/delivery", tags=["delivery"])


@router.post("/", response_model=DeliveryTracking, status_code=201)
async def create_delivery(
    data: DeliveryTrackingCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Create new delivery tracking record."""
    tracking = await create_delivery_tracking(db, data, current_user.id)
    if not tracking:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_ERROR,
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
    return tracking


@router.get("/order/{order_id}", response_model=List[DeliveryTracking])
async def get_delivery_by_order(
    order_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Get all delivery tracking records for an order."""
    trackings = await get_delivery_trackings_by_order(db, order_id)
    return trackings


@router.put("/{tracking_id}/status", response_model=DeliveryTracking)
async def update_delivery_status_endpoint(
    tracking_id: int,
    status: str,
    location: str = None,
    notes: str = None,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Update delivery tracking status."""
    tracking = await update_delivery_status(
        db, tracking_id, status, current_user.id, location, notes
    )
    if not tracking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery tracking not found",
        )
    return tracking
