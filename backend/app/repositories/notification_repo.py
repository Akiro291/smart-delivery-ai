"""
Notification repository with CRUD operations.
"""

from typing import Any

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.notification import Notification, NotificationStatus


async def create_notification(
    db: AsyncSession,
    data: dict[str, Any],
) -> Notification:
    """Create a new notification."""
    notification = Notification(
        user_id=data["user_id"],
        type=data["type"],
        status=data.get("status", NotificationStatus.PENDING),
        title=data["title"],
        message=data["message"],
        meta_data=data.get("meta_data"),
    )
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    return notification


async def get_notification_by_id(
    db: AsyncSession,
    notification_id: int,
) -> Notification | None:
    """Get notification by ID."""
    return await db.get(Notification, notification_id)


async def get_notifications_by_user(
    db: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    status_filter: NotificationStatus | None = None,
) -> list[Notification]:
    """Get notifications for a user with optional status filter."""
    query = select(Notification).where(Notification.user_id == user_id)
    if status_filter:
        query = query.where(Notification.status == status_filter)
    query = query.offset(skip).limit(limit).order_by(Notification.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def update_notification(
    db: AsyncSession,
    notification_id: int,
    status: NotificationStatus,
) -> Notification | None:
    """Update notification status."""
    notification = await get_notification_by_id(db, notification_id)
    if not notification:
        return None
    notification.status = status
    await db.commit()
    await db.refresh(notification)
    return notification


async def mark_as_read(
    db: AsyncSession,
    notification_id: int,
) -> Notification | None:
    """Mark notification as read."""
    return await update_notification(db, notification_id, NotificationStatus.READ)


async def get_unread_count(
    db: AsyncSession,
    user_id: int,
) -> int:
    """Get count of unread notifications for a user."""
    result = await db.execute(
        select(func.count()).select_from(Notification).where(
            Notification.user_id == user_id,
            Notification.status != NotificationStatus.READ,
        )
    )
    return result.scalar_one()


async def mark_all_as_read(
    db: AsyncSession,
    user_id: int,
) -> int:
    """Mark all notifications as read for a user. Returns count of updated notifications."""
    result = await db.execute(
        select(Notification.id).where(
            Notification.user_id == user_id,
            Notification.status != NotificationStatus.READ,
        )
    )
    ids = result.scalars().all()
    
    if ids:
        await db.execute(
            update(Notification).where(
                Notification.id.in_(ids),
                Notification.status != NotificationStatus.READ,
            ).values(status=NotificationStatus.READ)
        )
        await db.commit()
    
    return len(ids)
