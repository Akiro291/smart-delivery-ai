"""
Order history models for tracking order changes.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from app.db.base import Base, IDMixin, TimestampMixin
from app.db.models.order import OrderStatus


class OrderHistory(Base, IDMixin, TimestampMixin):
    """Order history model for tracking status changes."""
    
    __tablename__ = "order_history"
    
    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )
    from_status = Column(
        SQLEnum(OrderStatus),
        nullable=True
    )
    to_status = Column(
        SQLEnum(OrderStatus),
        nullable=False
    )
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = Column(String(500), nullable=True)