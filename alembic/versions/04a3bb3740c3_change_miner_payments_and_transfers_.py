"""Change miner payments and transfers primary keys to include block number

Revision ID: 04a3bb3740c3
Revises: a10d68643476
Create Date: 2021-11-02 22:42:01.702538

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "04a3bb3740c3"
down_revision = "a10d68643476"
branch_labels = None
depends_on = None


def upgrade():
    # transfers
    op.execute("ALTER TABLE transfers DROP CONSTRAINT transfers_pkey")
    op.create_primary_key(
        "transfers_pkey",
        "transfers",
        ["block_number", "transaction_hash", "trace_address"],
    )
    op.drop_index("ix_transfers_block_number")

    # miner_payments
    op.execute("ALTER TABLE miner_payments DROP CONSTRAINT miner_payments_pkey")
    op.create_primary_key(
        "miner_payments_pkey",
        "miner_payments",
        ["block_number", "transaction_hash"],
    )
    op.drop_index("ix_block_number")


def downgrade():
    # transfers
    op.execute("ALTER TABLE transfers DROP CONSTRAINT transfers_pkey")
    op.create_index("ix_transfers_block_number", "transfers", ["block_number"])
    op.create_primary_key(
        "transfers_pkey",
        "transfers",
        ["transaction_hash", "trace_address"],
    )

    # miner_payments
    op.execute("ALTER TABLE miner_payments DROP CONSTRAINT miner_payments_pkey")
    op.create_index("ix_block_number", "miner_payments", ["block_number"])
    op.create_primary_key(
        "miner_payments_pkey",
        "miner_payments",
        ["transaction_hash"],
    )
