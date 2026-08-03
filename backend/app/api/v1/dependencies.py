"""
Dependencies for auth and authorization.
"""

from typing import TYPE_CHECKING, List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.security import verify_token
from app.repositories.user_repo import get_user_by_id

if TYPE_CHECKING:
    from app.db.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    db: AsyncSession = Depends(get_async_session),
    token: str = Depends(oauth2_scheme),
) -> "User":
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token)
    if not payload:
        raise credentials_exception
    user_id = payload.get("sub")
    if not user_id:
        raise credentials_exception
    user = await get_user_by_id(db, user_id=int(user_id))
    if not user:
        raise credentials_exception
    return user


def decode_token(token: str) -> dict | None:
    return verify_token(token)


def require_role(allowed_roles: List[str]):
    """Dependency factory to check if current user has one of the allowed roles."""
    async def role_checker(current_user: "User" = Depends(get_current_user)) -> "User":
        if current_user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user
    return role_checker


def require_any_role(allowed_roles: List[str]):
    """Dependency to check if current user has any of the allowed roles.
    
    This is an alias for require_role for backward compatibility.
    """
    return require_role(allowed_roles)


def require_admin(current_user: "User" = Depends(require_role(["ADMIN"]))):
    """Dependency to check if current user has ADMIN role."""
    return current_user
