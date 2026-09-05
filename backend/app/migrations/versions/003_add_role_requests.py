"""add role_requests table

Revision ID: 003_add_role_requests
Revises: 002_add_products_cart
Create Date: 2026-08-02 15:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "003_add_role_requests"
down_revision: str | None = "002_add_products_cart"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Create role_requests table
    op.create_table(
        "role_requests",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, unique=True),
        sa.Column("requested_role", sa.Enum("CUSTOMER", "COURIER", "ADMIN", name="userrole"), nullable=False),
        sa.Column("status", sa.Enum("PENDING", "APPROVED", "REJECTED", name="rolerequeststatus"), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("reviewed_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Create indexes
    op.create_index(op.f("ix_role_requests_user_id"), "role_requests", ["user_id"], unique=True)
    op.create_index(op.f("ix_role_requests_status"), "role_requests", ["status"], unique=False)


def downgrade() -> None:
    op.drop_table("role_requests")
