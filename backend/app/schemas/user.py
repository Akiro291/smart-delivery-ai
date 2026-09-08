"""
User schemas for the application.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.db.models.user import RoleRequestStatus, UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    phone: str | None = None
    role: UserRole = UserRole.CUSTOMER


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str | None = None
    phone: str | None = None
    password: str
    role: UserRole = UserRole.CUSTOMER


class UserUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None


class UserUpdateRole(BaseModel):
    role: UserRole


class UserUpdateUserStatus(BaseModel):
    is_active: bool


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime | None = None


class RoleRequestCreate(BaseModel):
    requested_role: UserRole
    reason: str | None = None


class RoleRequestUpdate(BaseModel):
    status: RoleRequestStatus
    reason: str | None = None


class RoleRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    requested_role: UserRole
    status: RoleRequestStatus
    reason: str | None = None
    reviewed_by: int | None = None
    reviewed_at: datetime | None = None
    created_at: datetime | None = None


class RoleRequestWithUser(RoleRequest):
    model_config = ConfigDict(from_attributes=True)

    user_email: str | None = None
    user_full_name: str | None = None
