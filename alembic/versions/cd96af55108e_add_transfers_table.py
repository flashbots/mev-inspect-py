"""Add transfers table

Revision ID: cd96af55108e
Revises: 5437dc68f4df
Create Date: 2021-09-17 12:44:45.245137

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "cd96af55108e"
down_revision = "320e56b0a99f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "transfers",
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("block_number", sa.Numeric, nullable=False),
        sa.Column("transaction_hash", sa.String(66), nullable=False),
        sa.Column("trace_address", sa.String(256), nullable=False),
        sa.Column("protocol", sa.String(256), nullable=True),
        sa.Column("from_address", sa.String(256), nullable=False),
        sa.Column("to_address", sa.String(256), nullable=False),
        sa.Column("token_address", sa.String(256), nullable=False),
        sa.Column("amount", sa.Numeric, nullable=False),
        sa.Column("error", sa.String(256), nullable=True),
        sa.PrimaryKeyConstraint("transaction_hash", "trace_address"),
    )
    op.create_index("ix_transfers_block_number", "transfers", ["block_number"])


def downgrade():
    op.drop_index("ix_transfers_block_number", "transfers")
    op.drop_table("transfers")
