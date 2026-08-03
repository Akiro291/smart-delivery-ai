"""
Alembic migration configuration for async SQLAlchemy.
"""

import sys
import os
from logging.config import fileConfig

from sqlalchemy import pool, event
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Add backend folder to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.core.config import settings  # noqa: E402
from app.db.base import Base  # noqa: E402

# Import models directly to avoid circular imports
from app.db.models.user import User, UserRole, RoleRequest, RoleRequestStatus  # noqa: E402
from app.db.models.order import Order, OrderStatus  # noqa: E402
from app.db.models.order_history import OrderHistory  # noqa: E402
from app.db.models.delivery_tracking import DeliveryTracking  # noqa: E402
from app.db.models.notification import Notification, NotificationType, NotificationStatus  # noqa: E402
from app.db.models.product import Product  # noqa: E402
from app.db.models.order_item import OrderItem, CartItem  # noqa: E402

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the database URL from settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Target metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """Run migrations with connection."""
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio  # noqa: E402

    asyncio.run(run_migrations_online())
