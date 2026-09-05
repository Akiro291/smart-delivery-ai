"""
Delivery tracking models.
"""

from sqlalchemy import Column, Float, ForeignKey, Integer

from app.db.base import Base, IDMixin, TimestampMixin


class DeliveryTracking(Base, IDMixin, TimestampMixin):
    """Delivery tracking model for real-time location tracking."""

    __tablename__ = "delivery_tracking"

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)
    current_lat = Column(Float, nullable=True)
    current_lon = Column(Float, nullable=True)
    last_updated = Column(Integer, nullable=True)
    estimated_delivery_time = Column(Integer, nullable=True)  # in minutes
    delivery_progress = Column(Integer, default=0)  # percentage
