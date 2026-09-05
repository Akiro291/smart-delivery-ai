"""
Cart and OrderItem schemas.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemCreate(CartItemBase):
    pass


class CartItem(CartItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime | None = None


class CartItemWithProduct(CartItem):
    product_name: str
    product_price: float
    product_image_url: str | None = None


class OrderItemBase(BaseModel):
    product_id: int
    product_name: str
    quantity: int = 1
    price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    created_at: datetime | None = None
