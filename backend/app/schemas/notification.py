"""
Notification schemas.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.db.models.notification import NotificationStatus, NotificationType


class NotificationBase(BaseModel):
    title: str
    message: str
    type: NotificationType = NotificationType.TELEGRAM
    meta_data: str | None = None


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    status: NotificationStatus | None = None


class Notification(NotificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: NotificationStatus = NotificationStatus.PENDING
    created_at: datetime | None = None
    updated_at: datetime | None = None
