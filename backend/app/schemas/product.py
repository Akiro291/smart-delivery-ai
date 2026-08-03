"""
Product schemas for the application.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    is_available: bool = True
    stock_quantity: int = 0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None
    stock_quantity: Optional[int] = None


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_url: Optional[str] = None
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
