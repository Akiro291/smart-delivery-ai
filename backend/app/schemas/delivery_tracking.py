"""
Delivery tracking schemas.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DeliveryTrackingBase(BaseModel):
    order_id: int
    current_lat: float | None = None
    current_lon: float | None = None
    estimated_delivery_time: int | None = None  # in minutes
    delivery_progress: int = 0  # percentage


class DeliveryTrackingCreate(DeliveryTrackingBase):
    pass


class DeliveryTrackingUpdate(BaseModel):
    current_lat: float | None = None
    current_lon: float | None = None
    estimated_delivery_time: int | None = None
    delivery_progress: int | None = None


class DeliveryTracking(DeliveryTrackingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
