"""fix timestamps and role_requests enum

- notifications.sent_at: Integer -> timestamptz
- delivery_tracking.last_updated: Integer -> timestamptz
- userrole enum: ensure MANAGER value exists (role_requests inline enum drift)

Revision ID: 004_fix_timestamps
Revises: 003_add_role_requests
Create Date: 2026-09-08 12:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "004_fix_timestamps"
down_revision: str | None = "003_add_role_requests"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # notifications.sent_at: epoch seconds -> timestamptz
    op.execute(
        """
        ALTER TABLE notifications
        ALTER COLUMN sent_at TYPE timestamptz
        USING CASE
            WHEN sent_at IS NULL THEN NULL
            ELSE to_timestamp(sent_at::double precision)
        END
        """
    )

    # delivery_tracking.last_updated: epoch seconds -> timestamptz
    op.execute(
        """
        ALTER TABLE delivery_tracking
        ALTER COLUMN last_updated TYPE timestamptz
        USING CASE
            WHEN last_updated IS NULL THEN NULL
            ELSE to_timestamp(last_updated::double precision)
        END
        """
    )

    # The role_requests.requested_role column uses the shared "userrole" enum type,
    # but migration 003 declared it without the MANAGER value. Ensure it exists.
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'MANAGER'")


def downgrade() -> None:
    # Convert timestamps back to epoch seconds
    op.execute(
        """
        ALTER TABLE notifications
        ALTER COLUMN sent_at TYPE integer
        USING CASE
            WHEN sent_at IS NULL THEN NULL
            ELSE EXTRACT(EPOCH FROM sent_at)::integer
        END
        """
    )
    op.execute(
        """
        ALTER TABLE delivery_tracking
        ALTER COLUMN last_updated TYPE integer
        USING CASE
            WHEN last_updated IS NULL THEN NULL
            ELSE EXTRACT(EPOCH FROM last_updated)::integer
        END
        """
    )
    # Note: MANAGER value in userrole is intentionally NOT removed on downgrade
    # because users.role may already reference it.
