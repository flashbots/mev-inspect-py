"""add_swap_jit_liquidity_join_table

Revision ID: ceb5976b37dd
Revises: 5c5375de15fd
Create Date: 2022-04-19 18:34:26.332094

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ceb5976b37dd"
down_revision = "5c5375de15fd"
branch_labels = None
depends_on = None


# This revision was swapped with adding_jit_liquidity_table because I created revisions in wrong order
def upgrade():
    op.create_table(
        "jit_liquidity",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("block_number", sa.Numeric(), nullable=False),
        sa.Column("bot_address", sa.String(42), nullable=True),
        sa.Column("pool_address", sa.String(42), nullable=False),
        sa.Column("token0_address", sa.String(42), nullable=True),
        sa.Column("token1_address", sa.String(42), nullable=True),
        sa.Column("mint_transaction_hash", sa.String(66), nullable=False),
        sa.Column("mint_transaction_trace", sa.ARRAY(sa.Integer)),
        sa.Column("burn_transaction_hash", sa.String(66), nullable=False),
        sa.Column("burn_transaction_trace", sa.ARRAY(sa.Integer)),
        sa.Column("mint_token0_amount", sa.Numeric),
        sa.Column("mint_token1_amount", sa.Numeric),
        sa.Column("burn_token0_amount", sa.Numeric),
        sa.Column("burn_token1_amount", sa.Numeric),
        sa.Column("token0_swap_volume", sa.Numeric),
        sa.Column("token1_swap_volume", sa.Numeric),
    )
    op.create_index("ix_jit_liquidity_block_number", "jit_liquidity", ["block_number"])


def downgrade():
    op.drop_index("ix_jit_liquidity_block_number")
    op.drop_table("jit_liquidity")
