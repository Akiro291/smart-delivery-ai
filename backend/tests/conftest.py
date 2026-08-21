"""
Test configuration and fixtures for backend tests.
"""

import re
from unittest.mock import patch

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings
from app.db.base import Base


def _replace_host(url: str, new_host: str) -> str:
    return re.sub(r"@([^:/]+)", f"@{new_host}", url)


@pytest.fixture(scope="session", autouse=True)
def override_settings():
    local_url = _replace_host(settings.DATABASE_URL, "localhost")
    test_database_url = local_url.replace("smart_delivery", "smart_delivery_test")
    with patch.object(settings, 'DATABASE_URL', test_database_url):
        yield


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    test_database_url = settings.DATABASE_URL
    admin_url = test_database_url.replace("smart_delivery_test", "postgres")

    admin_engine = create_async_engine(
        admin_url,
        echo=True,
        isolation_level="AUTOCOMMIT",
    )
    async with admin_engine.connect() as conn:
        try:
            await conn.execute(text("CREATE DATABASE smart_delivery_test"))
        except Exception:
            pass
    await admin_engine.dispose()

    engine = create_async_engine(
        test_database_url,
        echo=True,
        connect_args={"statement_cache_size": 0},
        pool_size=1,
        max_overflow=0,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine):
    """Create database session for tests."""
    async_session = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    session = async_session()
    try:
        yield session
    finally:
        await session.rollback()
        await session.close()
