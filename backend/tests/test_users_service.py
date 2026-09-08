"""Tests for user service layer."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User, UserRole
from app.repositories.user_repo import (
    create_role_request,
    get_role_request_by_user,
    get_user_by_email,
    update_role_request,
    update_user,
)
from app.schemas.user import UserCreate
from app.services.users_service import UserService


@pytest.mark.asyncio
async def test_create_user_hashes_password(db_session: AsyncSession):
    data = UserCreate(
        email="svc_user@example.com",
        password="strongpassword123",
        full_name="Test User",
    )
    service = UserService(db_session)
    user = await service.create_user(data)
    assert user.id is not None
    assert user.role == UserRole.CUSTOMER
    assert user.hashed_password != "strongpassword123"
    found = await get_user_by_email(db_session, user.email)
    assert found is not None


@pytest.mark.asyncio
async def test_update_user_profile(db_session: AsyncSession):
    user = User(email="svc_upd@example.com", hashed_password="x", full_name="Old Name")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    updated = await update_user(db_session, user, {"full_name": "New Name", "phone": "+79990001122"})
    assert updated.full_name == "New Name"
    assert updated.phone == "+79990001122"


@pytest.mark.asyncio
async def test_role_request_workflow(db_session: AsyncSession):
    user = User(email="svc_role@example.com", hashed_password="x")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    request = await create_role_request(db_session, user.id, "COURIER", "I want to deliver")
    assert request.status.value == "PENDING"
    assert request.requested_role == UserRole.COURIER

    found = await get_role_request_by_user(db_session, user.id)
    assert found is not None
    assert found.id == request.id

    approved = await update_role_request(db_session, request, "APPROVED", reviewed_by=1)
    assert approved.status.value == "APPROVED"
    assert approved.reviewed_at is not None
