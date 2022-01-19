"""Create mev_summary table

Revision ID: ab9a9e449ff9
Revises: b26ab0051a88
Create Date: 2022-01-18 18:36:42.865154

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ab9a9e449ff9"
down_revision = "b26ab0051a88"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "mev_summary",
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("block_number", sa.Numeric, nullable=False),
        sa.Column("block_timestamp", sa.TIMESTAMP, nullable=False),
        sa.Column("protocol", sa.String(256), nullable=True),
        sa.Column("transaction_hash", sa.String(66), nullable=False),
        sa.Column("type", sa.String(256), nullable=False),
        sa.Column("gross_profit_usd", sa.Numeric, nullable=False),
        sa.Column("miner_payment_usd", sa.Numeric, nullable=False),
        sa.Column("gas_used", sa.Numeric, nullable=False),
        sa.Column("gas_price", sa.Numeric, nullable=False),
        sa.Column("coinbase_transfer", sa.Numeric, nullable=False),
        sa.Column("gas_price_with_coinbase_transfer", sa.Numeric, nullable=False),
        sa.Column("miner_address", sa.String(256), nullable=False),
        sa.Column("base_fee_per_gas", sa.Numeric, nullable=False),
        sa.Column("error", sa.String(256), nullable=True),
    )


def downgrade():
    op.drop_table("mev_summary")
