"""Add block_number to nft_trades primary key

Revision ID: 5c5375de15fd
Revises: e616420acd18
Create Date: 2022-01-21 15:27:57.790340

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "5c5375de15fd"
down_revision = "e616420acd18"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE nft_trades DROP CONSTRAINT nft_trades_pkey")
    op.create_primary_key(
        "nft_trades_pkey",
        "nft_trades",
        ["block_number", "transaction_hash", "trace_address"],
    )


def downgrade():
    op.execute("ALTER TABLE nft_trades DROP CONSTRAINT nft_trades_pkey")
    op.create_primary_key(
        "nft_trades_pkey",
        "nft_trades",
        ["transaction_hash", "trace_address"],
    )
