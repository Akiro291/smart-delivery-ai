from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

_engine = None

AsyncSessionLocal = None


def get_engine():
    """Lazy engine creation to support settings changes (e.g. in tests)."""
    global _engine, AsyncSessionLocal, async_session_factory
    if _engine is None:
        _engine = create_async_engine(settings.database_url_async, echo=settings.DEBUG)
        AsyncSessionLocal = async_sessionmaker(
            _engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
        async_session_factory = AsyncSessionLocal
    return _engine


async_session_factory = None


async def get_async_session():
    """Dependency for getting database session."""
    get_engine()
    async with async_session_factory() as session:
        yield session


async def get_session() -> AsyncSession:
    """Dependency for getting database session."""
    get_engine()
    async with async_session_factory() as session:
        yield session


async def close_engine():
    """Close the async engine."""
    global _engine, AsyncSessionLocal, async_session_factory
    if _engine:
        await _engine.dispose()
        _engine = None
        AsyncSessionLocal = None
        async_session_factory = None
