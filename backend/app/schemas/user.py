"""
User schemas for the application.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from app.db.models.user import UserRole, RoleRequestStatus


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: UserRole = UserRole.CUSTOMER


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserUpdateRole(BaseModel):
    role: UserRole


class UserUpdateUserStatus(BaseModel):
    is_active: bool


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool = True
    is_superuser: bool = False
    created_at: Optional[datetime] = None


class RoleRequestCreate(BaseModel):
    requested_role: UserRole
    reason: Optional[str] = None


class RoleRequestUpdate(BaseModel):
    status: RoleRequestStatus
    reason: Optional[str] = None


class RoleRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    requested_role: UserRole
    status: RoleRequestStatus
    reason: Optional[str] = None
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None


class RoleRequestWithUser(RoleRequest):
    model_config = ConfigDict(from_attributes=True)

    user_email: Optional[str] = None
    user_full_name: Optional[str] = None
