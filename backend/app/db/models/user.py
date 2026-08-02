"""
User models for the application.
"""

from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from app.db.base import Base, IDMixin, TimestampMixin
from enum import Enum


class UserRole(str, Enum):
    """User roles enumeration."""
    CUSTOMER = "CUSTOMER"
    COURIER = "COURIER"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"


class User(Base, IDMixin, TimestampMixin):
    """User model."""
    
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    role = Column(
        SQLEnum(UserRole),
        default=UserRole.CUSTOMER,
        nullable=False
    )
    is_active = Column(Integer, default=1)
    is_superuser = Column(Integer, default=0)