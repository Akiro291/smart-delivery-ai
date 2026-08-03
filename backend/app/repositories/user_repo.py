"""
User repository with CRUD operations.
"""

from datetime import datetime
from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User, RoleRequest, RoleRequestStatus, UserRole
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Get user by email."""
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """Get user by ID."""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def get_user_by_phone(db: AsyncSession, phone: str) -> Optional[User]:
    """Get user by phone number."""
    result = await db.execute(
        select(User).where(User.phone == phone)
    )
    return result.scalar_one_or_none()


async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users with pagination."""
    result = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    return list(result.scalars().all())


async def get_user_count(db: AsyncSession) -> int:
    """Get total user count."""
    result = await db.execute(
        select(func.count()).select_from(User)
    )
    return result.scalar_one()


async def get_users_by_role(db: AsyncSession, role: str, skip: int = 0, limit: int = 100) -> List[User]:
    """Get users by role with pagination."""
    result = await db.execute(
        select(User)
        .where(User.role == UserRole(role))
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """Create a new user. Role is always set to CUSTOMER regardless of input."""
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        phone=user_data.phone,
        role=user_data.role,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(
    db: AsyncSession, user: User, user_data: dict
) -> User:
    """Update user fields."""
    for field, value in user_data.items():
        if value is not None and hasattr(user, field):
            setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user_role(db: AsyncSession, user: User, new_role: str) -> User:
    """Update user role. Only ADMIN can do this via endpoint."""
    user.role = UserRole(new_role)
    await db.commit()
    await db.refresh(user)
    return user


async def deactivate_user(db: AsyncSession, user_id: int) -> bool:
    """Deactivate a user."""
    user = await get_user_by_id(db, user_id)
    if user:
        user.is_active = False
        await db.commit()
    return bool(user)


async def activate_user(db: AsyncSession, user_id: int) -> Optional[User]:
    """Activate a user."""
    user = await get_user_by_id(db, user_id)
    if user:
        user.is_active = True
        await db.commit()
        await db.refresh(user)
    return user


async def create_role_request(db: AsyncSession, user_id: int, requested_role: str, reason: Optional[str] = None) -> RoleRequest:
    """Create a role request for a user."""
    requested_role_enum = UserRole(requested_role)
    
    # Check if there's already a pending request
    result = await db.execute(
        select(RoleRequest)
        .where(RoleRequest.user_id == user_id)
        .where(RoleRequest.status == RoleRequestStatus.PENDING)
    )
    existing = result.scalar_one_or_none()
    if existing:
        existing.requested_role = requested_role_enum
        existing.reason = reason
        await db.commit()
        await db.refresh(existing)
        return existing
    
    role_request = RoleRequest(
        user_id=user_id,
        requested_role=requested_role_enum,
        reason=reason,
    )
    db.add(role_request)
    await db.commit()
    await db.refresh(role_request)
    return role_request


async def get_role_requests(db: AsyncSession, status_filter: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[RoleRequest]:
    """Get role requests with optional status filter."""
    query = select(RoleRequest)
    if status_filter:
        query = query.where(RoleRequest.status == RoleRequestStatus(status_filter))
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_role_request_by_user(db: AsyncSession, user_id: int) -> Optional[RoleRequest]:
    """Get role request for a specific user."""
    result = await db.execute(
        select(RoleRequest)
        .where(RoleRequest.user_id == user_id)
        .where(RoleRequest.status == RoleRequestStatus.PENDING)
    )
    return result.scalar_one_or_none()


async def update_role_request(db: AsyncSession, request: RoleRequest, status: str, reviewed_by: int, reason: Optional[str] = None) -> RoleRequest:
    """Update role request status."""
    request.status = RoleRequestStatus(status)
    request.reviewed_by = reviewed_by
    request.reviewed_at = datetime.utcnow()
    if reason:
        request.reason = reason
    await db.commit()
    await db.refresh(request)
    return request
