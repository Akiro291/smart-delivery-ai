"""
Cart and order items models.
"""

from sqlalchemy import Column, Float, ForeignKey, Integer, String

from app.db.base import Base, IDMixin, TimestampMixin


class CartItem(Base, IDMixin, TimestampMixin):
    """Shopping cart item."""

    __tablename__ = "cart_items"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)


class OrderItem(Base, IDMixin, TimestampMixin):
    """Order line item - links order to product."""

    __tablename__ = "order_items"

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)
