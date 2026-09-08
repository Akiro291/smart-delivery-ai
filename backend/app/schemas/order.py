"""
Order schemas for the application.
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.db.models.order import OrderStatus


class OrderBase(BaseModel):
    from_address: str
    to_address: str
    total_amount: Decimal
    description: str | None = None
    is_priority: bool = False


class OrderItemCreate(BaseModel):
    product_id: int
    product_name: str
    quantity: int = 1
    price: float


class OrderCreate(OrderBase):
    items: list[OrderItemCreate] | None = None


class OrderUpdate(BaseModel):
    status: OrderStatus | None = None
    courier_id: int | None = None
    description: str | None = None


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    courier_id: int | None = None
    status: OrderStatus = OrderStatus.PENDING
    customer_name: str | None = None
    courier_name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class OrderHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    from_status: str | None = None
    to_status: str
    changed_by: int | None = None
    notes: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
