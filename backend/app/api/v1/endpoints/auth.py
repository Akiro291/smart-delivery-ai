"""
Authentication endpoints.
"""

from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_async_session
from app.core.security import (
    create_access_token,
    verify_password,
    get_password_hash,
)
from app.repositories.user_repo import (
    create_user,
    get_user_by_email,
    get_user_by_id,
)
from app.db.models.user import User
from app.schemas.user import UserCreate, User
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


class ResetPasswordRequest(BaseModel):
    email: str


class RegisterResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: User


@router.post("/register", response_model=RegisterResponse)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_async_session),
):
    db_user = await get_user_by_email(db, email=user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    new_user = await create_user(db, user_data)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_ERROR,
            detail="Error creating user",
        )
    access_token = create_access_token(
        subject=str(new_user.id),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_access_token(
        subject=str(new_user.id),
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": User.model_validate(new_user),
    }


@router.post("/login", response_model=dict)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
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
    refresh_token = create_access_token(
        subject=str(user.id),
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": User.model_validate(user),
    }


@router.get("/me", response_model=User)
async def get_current_user_endpoint(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.post("/reset-password")
async def reset_password(
    body: ResetPasswordRequest,
    db: AsyncSession = Depends(get_async_session),
):
    user = await get_user_by_email(db, email=body.email)
    if not user:
        return {"message": "If the email exists, a reset link has been sent"}
    token = create_access_token(
        subject=str(user.id),
        expires_delta=timedelta(hours=24),
    )
    return {"message": "If the email exists, a reset link has been sent"}
