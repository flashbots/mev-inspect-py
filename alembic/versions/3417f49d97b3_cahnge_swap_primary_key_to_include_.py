"""Cahnge swap primary key to include block number

Revision ID: 3417f49d97b3
Revises: 205ce02374b3
Create Date: 2021-11-02 20:50:32.854996

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "3417f49d97b3"
down_revision = "205ce02374b3"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE swaps DROP CONSTRAINT swaps_pkey CASCADE")
    op.create_primary_key(
        "swaps_pkey",
        "swaps",
        ["block_number", "transaction_hash", "trace_address"],
    )
    op.create_index(
        "arbitrage_swaps_swaps_idx",
        "arbitrage_swaps",
        ["swap_transaction_hash", "swap_trace_address"],
    )


def downgrade():
    op.drop_index("arbitrage_swaps_swaps_idx")
    op.execute("ALTER TABLE swaps DROP CONSTRAINT swaps_pkey CASCADE")
    op.create_primary_key(
        "swaps_pkey",
        "swaps",
        ["transaction_hash", "trace_address"],
    )
    op.create_foreign_key(
        "arbitrage_swaps_swaps_fkey",
        "arbitrage_swaps",
        "swaps",
        ["swap_transaction_hash", "swap_trace_address"],
        ["transaction_hash", "trace_address"],
    )
