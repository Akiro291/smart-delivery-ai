"""
Authentication endpoints.
"""

import secrets
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.core.config import settings
from app.core.database import get_async_session
from app.core.logging import get_logger
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    verify_token,
)
from app.db.models.user import User as UserModel
from app.db.models.user import UserRole
from app.repositories.user_repo import (
    create_user,
    get_user_by_email,
    get_user_by_id,
)
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


class ResetPasswordRequest(BaseModel):
    email: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserSchema | None = None


class RegisterResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserSchema


class RefreshRequest(BaseModel):
    refresh_token: str


async def _enforce_auth_rate_limit(request: Request, action: str) -> None:
    """Per-IP fixed-window rate limit for auth endpoints (best-effort)."""
    from app.core.redis import rate_limit_hit

    client_ip = request.client.host if request.client else "unknown"
    if await rate_limit_hit(f"auth:{action}:{client_ip}", limit=20, window_seconds=300):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Try again later.",
        )


@router.post("/register", response_model=RegisterResponse)
async def register(
    user_data: UserCreate,
    request: Request,
    db: AsyncSession = Depends(get_async_session),
):
    await _enforce_auth_rate_limit(request, "register")
    db_user = await get_user_by_email(db, email=user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    # Force role to CUSTOMER for all new registrations
    user_data.role = UserRole.CUSTOMER
    new_user = await create_user(db, user_data)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user",
        )
    access_token = create_access_token(
        subject=str(new_user.id),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(
        subject=str(new_user.id),
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": UserSchema.model_validate(new_user),
    }


@router.post("/login", response_model=TokenResponse)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
    await _enforce_auth_rate_limit(request, "login")
    user = await get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(
        subject=str(user.id),
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": UserSchema.model_validate(user),
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(
    body: RefreshRequest,
    db: AsyncSession = Depends(get_async_session),
):
    """Refresh access token using refresh token."""
    payload = verify_token(body.refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check that this is actually a refresh token
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = await get_user_by_id(db, user_id=int(user_id))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    # Issue new tokens
    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    new_refresh_token = create_refresh_token(
        subject=str(user.id),
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserSchema)
async def get_current_user_endpoint(
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_user),
):
    return current_user


@router.post("/reset-password")
async def reset_password(
    body: ResetPasswordRequest,
    db: AsyncSession = Depends(get_async_session),
):
    """Request a password reset. Always returns a generic message."""
    from app.core.redis import rate_limit_hit, store_reset_token

    # Simple per-email rate limit: 5 requests per hour
    if await rate_limit_hit(f"pwd_reset:{body.email.lower()}", limit=5, window_seconds=3600):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many reset requests. Try again later.",
        )

    generic_response = {"message": "If the email exists, a reset link has been sent"}
    user = await get_user_by_email(db, email=body.email)
    if not user or not user.is_active:
        return generic_response

    token = secrets.token_urlsafe(32)
    await store_reset_token(token, user.id)

    # Fire the email task (no-op failure if broker/SMTP unavailable); keep it
    # best-effort so a missing broker never blocks the API response.
    try:
        from app.tasks import celery_app

        celery_app.send_task(
            "app.tasks.notification.send_email",
            kwargs={
                "to_email": user.email,
                "subject": "Восстановление пароля — Smart Delivery",
                "body": (
                    f"Здравствуйте!\n\nЗапрос на восстановление пароля.\n"
                    f"Токен: {token}\n\nЕсли это были не вы — проигнорируйте письмо."
                ),
            },
        )
    except Exception as exc:  # pragma: no cover - broker failure path
        logger.warning(f"Could not queue reset email: {exc}")

    return generic_response


class ResetPasswordConfirmRequest(BaseModel):
    token: str
    new_password: str


@router.post("/reset-password/confirm")
async def reset_password_confirm(
    body: ResetPasswordConfirmRequest,
    db: AsyncSession = Depends(get_async_session),
):
    """Complete password reset using a single-use token."""
    from app.core.redis import consume_reset_token

    if len(body.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters",
        )
    user_id = await consume_reset_token(body.token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )
    user = await get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )
    user.hashed_password = get_password_hash(body.new_password)
    await db.commit()
    return {"message": "Password updated"}
