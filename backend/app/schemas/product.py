"""
Product schemas for the application.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: str | None = None
    is_available: bool = True
    stock_quantity: int = 0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category: str | None = None
    is_available: bool | None = None
    stock_quantity: int | None = None


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_url: str | None = None
    created_by: int | None = None
    created_at: datetime | None = None
