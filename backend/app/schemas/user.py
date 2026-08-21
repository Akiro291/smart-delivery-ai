"""
User schemas for the application.
"""

from datetime import datetime
from typing import Optional, Any, Union

from pydantic import BaseModel, ConfigDict, EmailStr, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

from app.db.models.user import UserRole, RoleRequestStatus


class UserRoleStr(str):
    """Pydantic type that accepts UserRole enum and serializes as string."""
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler) -> CoreSchema:
        def _validate(value: Any) -> str:
            if isinstance(value, UserRole):
                return value.name
            return str(value)
        return core_schema.with_info_plain_validator_function(
            lambda v, h: _validate(v)
        )


class RoleRequestStatusStr(str):
    """Pydantic type that accepts RoleRequestStatus enum and serializes as string."""
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler) -> CoreSchema:
        def _validate(value: Any) -> str:
            if isinstance(value, RoleRequestStatus):
                return value.name
            return str(value)
        return core_schema.with_info_plain_validator_function(
            lambda v, h: _validate(v)
        )


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: UserRole = UserRole.CUSTOMER


class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
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
    requested_role: UserRoleStr
    status: RoleRequestStatusStr
    reason: Optional[str] = None
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None


class RoleRequestWithUser(RoleRequest):
    model_config = ConfigDict(from_attributes=True)

    user_email: Optional[str] = None
    user_full_name: Optional[str] = None
