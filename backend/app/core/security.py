"""
Security utilities for authentication and authorization.
"""

from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
import bcrypt
import hashlib
from app.core.config import settings


def get_password_hash(password: str) -> str:
    """
    Get password hash using bcrypt.
    Handles passwords longer than 72 bytes by SHA256 pre-hashing.
    """
    password_bytes = password.encode('utf-8')
    
    # If password is longer than 72 bytes, hash it first with SHA256
    if len(password_bytes) > 72:
        password_bytes = hashlib.sha256(password_bytes).digest()
    
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    plain_bytes = plain_password.encode('utf-8')
    
    # If plain password is longer than 72 bytes, hash it first with SHA256
    if len(plain_bytes) > 72:
        plain_bytes = hashlib.sha256(plain_bytes).digest()
    
    return bcrypt.checkpw(plain_bytes, hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password)


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """Create JWT access token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """Create JWT refresh token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> dict:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.JWTError:
        return None
