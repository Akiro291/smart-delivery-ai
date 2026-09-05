"""
Notifications endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.core.database import get_async_session
from app.db.models.user import User as UserModel
from app.schemas.notification import Notification, NotificationCreate
from app.services.notifications_service import (
    create_notification,
    get_notification_by_id,
    get_unread_notifications_count,
    get_user_notifications,
    mark_all_notifications_read,
    mark_notification_read,
)

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/", response_model=list[Notification])
async def list_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status_filter: str | None = Query(None),
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Get notifications for current user."""
    notifications = await get_user_notifications(db, current_user.id, skip, limit, status_filter)
    return notifications


@router.get("/unread-count", response_model=int)
async def get_unread_count(
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Get count of unread notifications."""
    return await get_unread_notifications_count(db, current_user.id)


@router.get("/{notification_id}", response_model=Notification)
async def get_notification(
    notification_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Get notification by ID."""
    notification = await get_notification_by_id(db, notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return notification


@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED)
async def create_notification_endpoint(
    data: NotificationCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Create a new notification."""
    notification_data = data.model_dump()
    notification_data["user_id"] = current_user.id
    notification = await create_notification(db, notification_data)
    return notification


@router.patch("/{notification_id}/read", response_model=Notification)
async def mark_as_read(
    notification_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Mark notification as read."""
    notification = await get_notification_by_id(db, notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    updated = await mark_notification_read(db, notification_id)
    return updated


@router.post("/mark-all-read", response_model=dict)
async def mark_all_as_read_endpoint(
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Mark all notifications as read."""
    count = await mark_all_notifications_read(db, current_user.id)
    return {"message": f"Marked {count} notifications as read"}
