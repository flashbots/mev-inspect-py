"""Add swap arbitrage join table

Revision ID: 9b8ae51c5d56
Revises: 7eec417a4f3e
Create Date: 2021-08-06 17:06:55.364516

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9b8ae51c5d56"
down_revision = "7eec417a4f3e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "arbitrage_swaps",
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("arbitrage_id", sa.String(1024), primary_key=True),
        sa.Column("swap_transaction_hash", sa.String(66), primary_key=True),
        sa.Column("swap_trace_address", sa.ARRAY(sa.Integer), primary_key=True),
        sa.ForeignKeyConstraint(
            ["arbitrage_id"], ["arbitrages.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["swap_transaction_hash", "swap_trace_address"],
            ["swaps.transaction_hash", "swaps.trace_address"],
            ondelete="CASCADE",
        ),
    )


def downgrade():
    op.drop_table("arbitrage_swaps")
