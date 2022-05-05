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


# This revision is switched with add_swap_jit_liquidity_table becasue I made them in the wrong order
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
