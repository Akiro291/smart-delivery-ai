"""Tests for security utilities: password hashing and JWT tokens."""

import pytest

from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    verify_token,
)


def test_password_hash_roundtrip():
    hashed = get_password_hash("s3cret-password")
    assert hashed != "s3cret-password"
    assert verify_password("s3cret-password", hashed)
    assert not verify_password("wrong-password", hashed)


def test_password_hash_is_salted():
    h1 = get_password_hash("same-password")
    h2 = get_password_hash("same-password")
    assert h1 != h2


def test_access_token_roundtrip():
    token = create_access_token(subject="42")
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "42"
    assert "type" not in payload or payload.get("type") != "refresh"


def test_refresh_token_has_type():
    token = create_refresh_token(subject="42")
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "42"
    assert payload["type"] == "refresh"


def test_invalid_token_returns_none():
    assert verify_token("not-a-token") is None
    assert verify_token("") is None


def test_tampered_token_returns_none():
    token = create_access_token(subject="42")
    assert verify_token(token + "x") is None


@pytest.mark.asyncio
async def test_expired_token_returns_none():
    from datetime import timedelta

    token = create_access_token(subject="42", expires_delta=timedelta(seconds=-10))
    assert verify_token(token) is None
