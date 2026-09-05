"""
Notifications service layer.
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.notification import Notification, NotificationStatus
from app.repositories.notification_repo import (
    create_notification as _create_notification,
)
from app.repositories.notification_repo import (
    get_notification_by_id as _get_notification_by_id,
)
from app.repositories.notification_repo import (
    get_notifications_by_user as _get_notifications_by_user,
)
from app.repositories.notification_repo import (
    get_unread_count as _get_unread_count,
)
from app.repositories.notification_repo import (
    mark_all_as_read as _mark_all_as_read,
)
from app.repositories.notification_repo import (
    mark_as_read as _mark_as_read,
)


def _notification_to_dict(notification: Notification | None) -> dict[str, Any] | None:
    """Convert SQLAlchemy model to dict."""
    if notification is None:
        return None
    return {
        "id": notification.id,
        "user_id": notification.user_id,
        "type": notification.type.value if notification.type else None,
        "status": notification.status.value if notification.status else None,
        "title": notification.title,
        "message": notification.message,
        "meta_data": notification.meta_data,
        "created_at": notification.created_at,
        "updated_at": notification.updated_at,
    }


async def create_notification(
    db: AsyncSession,
    data: dict[str, Any],
) -> dict[str, Any]:
    """Create a new notification."""
    notification = await _create_notification(db, data)
    return _notification_to_dict(notification)


async def get_notification_by_id(
    db: AsyncSession,
    notification_id: int,
) -> dict[str, Any] | None:
    """Get notification by ID."""
    notification = await _get_notification_by_id(db, notification_id)
    return _notification_to_dict(notification)


async def get_user_notifications(
    db: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    status_filter: str | None = None,
) -> list[dict[str, Any]]:
    """Get notifications for a user."""
    status_enum = None
    if status_filter:
        try:
            status_enum = NotificationStatus(status_filter)
        except ValueError:
            pass
    notifications = await _get_notifications_by_user(db, user_id, skip, limit, status_enum)
    return [_notification_to_dict(n) for n in notifications]


async def mark_notification_read(
    db: AsyncSession,
    notification_id: int,
) -> dict[str, Any] | None:
    """Mark notification as read."""
    notification = await _mark_as_read(db, notification_id)
    return _notification_to_dict(notification)


async def mark_all_notifications_read(
    db: AsyncSession,
    user_id: int,
) -> int:
    """Mark all notifications as read for a user."""
    return await _mark_all_as_read(db, user_id)


async def get_unread_notifications_count(
    db: AsyncSession,
    user_id: int,
) -> int:
    """Get count of unread notifications for a user."""
    return await _get_unread_count(db, user_id)
