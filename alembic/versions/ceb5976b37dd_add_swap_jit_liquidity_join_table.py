"""add_swap_jit_liquidity_join_table

Revision ID: ceb5976b37dd
Revises: 5c5375de15fd
Create Date: 2022-04-19 18:34:26.332094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ceb5976b37dd'
down_revision = '5c5375de15fd'
branch_labels = None
depends_on = None


def upgrade():
    sa.create_table(
        "jit_liquidity_swaps",
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("jit_liquidity_id", sa.String(1024), primary_key=True),
        sa.Column("swap_transaction_hash", sa.String(66), primary_key=True),
        sa.Column("swap_trace_address", sa.ARRAY(sa.Integer), primary_key=True),
        sa.ForeignKeyConstraint(
            ["jit_liquidity_id"], ["jit_liquidity.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["swap_transaction_hash", "swap_trace_address"],
            ["swaps.transaction_hash", "swaps.trace_address"],
            ondelete="CASCADE",
        )
    )


def downgrade():
    op.drop_table("jit_liquidity_swaps")
