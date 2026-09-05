"""
Users service package.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.repositories.user_repo import get_user_by_id, get_user_by_email, update_user


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

    async def update_user_profile(self, user: User, data: dict) -> User:
        """Update user profile information."""
        return await update_user(self.db, user, data)
