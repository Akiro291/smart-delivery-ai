"""
Order models for the application.
"""

from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.db.base import Base, IDMixin, TimestampMixin


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

    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    courier_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    from_address = Column(String(500), nullable=False)
    to_address = Column(String(500), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    description = Column(String(1000), nullable=True)
    is_priority = Column(Integer, default=0)

    customer = relationship("User", foreign_keys=[customer_id], lazy="selectin")
    courier = relationship("User", foreign_keys=[courier_id], lazy="selectin")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy="selectin")
    history = relationship("OrderHistory", back_populates="order", cascade="all, delete-orphan", lazy="noload")
    tracking = relationship("DeliveryTracking", back_populates="order", uselist=False, lazy="selectin")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Order id={self.id} status={self.status}>"

    @property
    def customer_name(self) -> str | None:
        return (self.customer.full_name or self.customer.email) if self.customer else None

    @property
    def courier_name(self) -> str | None:
        return (self.courier.full_name or self.courier.email) if self.courier else None
