"""
Users service package.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.db.models.user import User
from app.repositories.user_repo import get_user_by_email, get_user_by_id, update_user
from app.schemas.user import UserCreate


class UserService:
    """Service for user-related operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user(self, user_id: int) -> User | None:
        """Get user by ID."""
        return await get_user_by_id(self.db, user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email."""
        return await get_user_by_email(self.db, email)

    async def create_user(self, data: UserCreate) -> User:
        """Create a new user with a hashed password (role forced to CUSTOMER upstream)."""
        hashed = get_password_hash(data.password)
        user = User(
            email=data.email,
            hashed_password=hashed,
            full_name=data.full_name,
            phone=data.phone,
            role=data.role,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user_profile(self, user: User, data: dict) -> User:
        """Update user profile information."""
        return await update_user(self.db, user, data)
