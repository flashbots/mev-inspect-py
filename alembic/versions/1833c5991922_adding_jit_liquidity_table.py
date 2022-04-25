"""adding jit liquidity table

Revision ID: 1833c5991922
Revises: ceb5976b37dd
Create Date: 2022-04-21 11:52:24.334825

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1833c5991922"
down_revision = "ceb5976b37dd"
branch_labels = None
depends_on = None


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
