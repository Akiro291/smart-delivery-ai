"""
Test configuration and fixtures for backend tests.
"""

import re
from unittest.mock import patch

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import app.db.models  # noqa: F401 - register all models on Base.metadata
from app.core.config import settings
from app.db.base import Base


def _replace_host(url: str, new_host: str) -> str:
    return re.sub(r"@([^:/]+)", f"@{new_host}", url)


@pytest.fixture(scope="session", autouse=True)
def override_settings():
    local_url = _replace_host(settings.DATABASE_URL, "localhost")
    # Normalize the database name so the fixture works both locally and in CI,
    # where DATABASE_URL may already point at smart_delivery_test.
    if not local_url.rsplit("/", 1)[-1].startswith("smart_delivery_test"):
        local_url = local_url.rsplit("/", 1)[0] + "/smart_delivery_test"
    with patch.object(settings, 'DATABASE_URL', local_url):
        yield


@pytest.fixture(scope="session")
async def _test_db_setup():
    """Create the test database once per session (schema only)."""
    test_database_url = settings.DATABASE_URL
    admin_url = test_database_url.rsplit("/", 1)[0] + "/postgres"

    admin_engine = create_async_engine(
        admin_url,
        isolation_level="AUTOCOMMIT",
    )
    async with admin_engine.connect() as conn:
        try:
            await conn.execute(text("CREATE DATABASE smart_delivery_test"))
        except Exception:
            pass
    await admin_engine.dispose()


@pytest.fixture
async def test_engine(_test_db_setup):
    """Create a fresh engine per test so connections bind to the current event loop."""
    engine = create_async_engine(
        settings.DATABASE_URL,
        connect_args={"statement_cache_size": 0},
        pool_size=1,
        max_overflow=0,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Clean all data so tests are idempotent against a persistent test DB
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE'))
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine):
    """Create database session for tests."""
    async_session = async_sessionmaker(test_engine, expire_on_commit=False)
    session = async_session()
    try:
        yield session
    finally:
        await session.rollback()
        await session.close()
