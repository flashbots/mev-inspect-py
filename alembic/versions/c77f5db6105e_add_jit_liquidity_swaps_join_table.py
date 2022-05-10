"""add_jit_liquidity_swaps_join_table

Revision ID: c77f5db6105e
Revises: a46974a623b3
Create Date: 2022-05-10 12:37:25.275799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c77f5db6105e'
down_revision = 'a46974a623b3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "jit_liquidity_swaps",
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("jit_liquidity_id", sa.String(1024), primary_key=True),
        sa.Column("swap_transaction_hash", sa.String(66), primary_key=True),
        sa.Column("swap_trace_address", sa.ARRAY(sa.Integer), primary_key=True),
        sa.ForeignKeyConstraint(
            ["jit_liquidity_id"], ["jit_liquidity.id"], ondelete="CASCADE"
        ),
    )


def downgrade():
    op.drop_table("jit_liquidity_swaps")
