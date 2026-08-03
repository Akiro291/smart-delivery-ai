"""
User models for the application.
"""

from sqlalchemy import Column, Integer, String, Enum as SQLEnum, Text, ForeignKey, DateTime, func
from app.db.base import Base, IDMixin, TimestampMixin
from enum import Enum


class UserRole(str, Enum):
    """User roles enumeration."""
    CUSTOMER = "CUSTOMER"
    COURIER = "COURIER"
    ADMIN = "ADMIN"


class RoleRequestStatus(str, Enum):
    """Role request statuses."""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


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


class RoleRequest(Base, IDMixin, TimestampMixin):
    """Role request model for users requesting role changes."""
    
    __tablename__ = "role_requests"
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    requested_role = Column(SQLEnum(UserRole), nullable=False)
    status = Column(SQLEnum(RoleRequestStatus), default=RoleRequestStatus.PENDING, nullable=False)
    reason = Column(Text, nullable=True)
    reviewed_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
