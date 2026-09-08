"""fix users boolean columns

- users.is_active: Integer -> Boolean
- users.is_superuser: Integer -> Boolean
Matches the SQLAlchemy model, which declares these as Boolean.

Revision ID: 005_users_boolean
Revises: 004_fix_timestamps
Create Date: 2026-09-08 13:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "005_users_boolean"
down_revision: str | None = "004_fix_timestamps"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TABLE users ALTER COLUMN is_active TYPE boolean USING is_active::int::boolean")
    op.execute("ALTER TABLE users ALTER COLUMN is_superuser TYPE boolean USING is_superuser::int::boolean")


def downgrade() -> None:
    op.execute("ALTER TABLE users ALTER COLUMN is_active TYPE integer USING is_active::int")
    op.execute("ALTER TABLE users ALTER COLUMN is_superuser TYPE integer USING is_superuser::int")
