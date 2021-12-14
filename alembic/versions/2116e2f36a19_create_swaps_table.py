"""Create swaps table

Revision ID: 2116e2f36a19
Revises: c5da44eb072c
Create Date: 2021-08-05 21:06:33.340456

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2116e2f36a19"
down_revision = "c5da44eb072c"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "swaps",
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("abi_name", sa.String(1024), nullable=False),
        sa.Column("transaction_hash", sa.String(66), nullable=False),
        sa.Column("block_number", sa.Numeric, nullable=False),
        sa.Column("trace_address", sa.String(256), nullable=False),
        sa.Column("protocol", sa.String(256), nullable=True),
        sa.Column("pool_address", sa.String(256), nullable=False),
        sa.Column("from_address", sa.String(256), nullable=False),
        sa.Column("to_address", sa.String(256), nullable=False),
        sa.Column("token_in_address", sa.String(256), nullable=False),
        sa.Column("token_in_amount", sa.Numeric, nullable=False),
        sa.Column("token_out_address", sa.String(256), nullable=False),
        sa.Column("token_out_amount", sa.Numeric, nullable=False),
        sa.PrimaryKeyConstraint("transaction_hash", "trace_address"),
    )


def downgrade():
    op.drop_table("swaps")
