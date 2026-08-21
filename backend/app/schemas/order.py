"""
Order schemas for the application.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.db.models.order import OrderStatus


class OrderBase(BaseModel):
    from_address: str
    to_address: str
    total_amount: Decimal
    description: Optional[str] = None
    is_priority: bool = False


class OrderCreate(OrderBase):
    customer_id: int


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    courier_id: Optional[int] = None
    description: Optional[str] = None


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    courier_id: Optional[int] = None
    status: OrderStatus = OrderStatus.PENDING
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class OrderHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    from_status: Optional[str] = None
    to_status: str
    changed_by: Optional[int] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
