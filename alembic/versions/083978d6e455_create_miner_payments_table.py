"""Create miner_payments table

Revision ID: 083978d6e455
Revises: 92f28a2b4f52
Create Date: 2021-08-30 17:42:25.548130

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "083978d6e455"
down_revision = "92f28a2b4f52"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "miner_payments",
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("block_number", sa.Numeric, nullable=False),
        sa.Column("transaction_hash", sa.String(66), primary_key=True),
        sa.Column("transaction_index", sa.Numeric, nullable=False),
        sa.Column("miner_address", sa.String(256), nullable=False),
        sa.Column("coinbase_transfer", sa.Numeric, nullable=False),
        sa.Column("base_fee_per_gas", sa.Numeric, nullable=False),
        sa.Column("gas_price", sa.Numeric, nullable=False),
        sa.Column("gas_price_with_coinbase_transfer", sa.Numeric, nullable=False),
        sa.Column("gas_used", sa.Numeric, nullable=False),
    )


def downgrade():
    op.drop_table("miner_payments")
