"""
Notification models.
"""

from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum

from app.db.base import Base, IDMixin, TimestampMixin


class NotificationType(str, Enum):
    """Notification type enumeration."""

    EMAIL = "EMAIL"
    TELEGRAM = "TELEGRAM"
    PUSH = "PUSH"
    SMS = "SMS"


class NotificationStatus(str, Enum):
    """Notification status enumeration."""

    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"
    READ = "READ"


class Notification(Base, IDMixin, TimestampMixin):
    """Notification model."""

    __tablename__ = "notifications"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(SQLEnum(NotificationType), nullable=False)
    status = Column(SQLEnum(NotificationStatus), default=NotificationStatus.PENDING, nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(String(1000), nullable=False)
    meta_data = Column(String(2000), nullable=True)
    sent_at = Column(Integer, nullable=True)
