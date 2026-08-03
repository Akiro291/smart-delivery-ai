"""
Product model for catalog.
"""

from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Boolean
from app.db.base import Base, IDMixin, TimestampMixin


class Product(Base, IDMixin, TimestampMixin):
    """Product model for catalog."""
    
    __tablename__ = "products"
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String(500), nullable=True)
    category = Column(String(100), nullable=True)
    is_available = Column(Boolean, default=True)
    stock_quantity = Column(Integer, default=0)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
