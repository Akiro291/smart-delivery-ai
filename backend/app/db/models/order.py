"""
Order models for the application.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum, Numeric
from app.db.base import Base, IDMixin, TimestampMixin
from app.db.models.user import UserRole
from enum import Enum


class OrderStatus(str, Enum):
    """Order status enumeration."""
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Order(Base, IDMixin, TimestampMixin):
    """Order model."""
    
    __tablename__ = "orders"
    
    customer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    courier_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )
    status = Column(
        SQLEnum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False
    )
    from_address = Column(String(500), nullable=False)
    to_address = Column(String(500), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    description = Column(String(1000), nullable=True)
    is_priority = Column(Integer, default=0)