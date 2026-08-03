"""
Set user as admin. Run with: python set_admin.py <email>
Example: python set_admin.py test123@gmail.com
"""
import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.core.database import async_session_factory
from app.db.models.user import User, UserRole
from app.repositories.user_repo import get_user_by_email


async def set_admin(email: str):
    async with async_session_factory() as db:
        user = await get_user_by_email(db, email=email)
        if not user:
            print(f"User with email {email} not found")
            return False
        
        user.role = UserRole.ADMIN
        user.is_superuser = 1
        user.is_active = True
        await db.commit()
        await db.refresh(user)
        
        print(f"User {user.email} is now ADMIN")
        print(f"Role: {user.role.name}")
        print(f"Is Superuser: {bool(user.is_superuser)}")
        print(f"Is Active: {bool(user.is_active)}")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python set_admin.py <email>")
        print("Example: python set_admin.py test123@gmail.com")
        sys.exit(1)
    
    email = sys.argv[1]
    result = asyncio.run(set_admin(email))
    sys.exit(0 if result else 1)
