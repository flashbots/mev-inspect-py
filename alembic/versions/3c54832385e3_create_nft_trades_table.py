"""Create NFT Trades table

Revision ID: 3c54832385e3
Revises: 4b9d289f2d74
Create Date: 2021-12-19 22:50:28.936516

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3c54832385e3"
down_revision = "4b9d289f2d74"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "nft_trades",
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("abi_name", sa.String(1024), nullable=False),
        sa.Column("transaction_hash", sa.String(66), nullable=False),
        sa.Column("transaction_position", sa.Numeric, nullable=False),
        sa.Column("block_number", sa.Numeric, nullable=False),
        sa.Column("trace_address", sa.String(256), nullable=False),
        sa.Column("protocol", sa.String(256), nullable=False),
        sa.Column("error", sa.String(256), nullable=True),
        sa.Column("seller_address", sa.String(256), nullable=False),
        sa.Column("buyer_address", sa.String(256), nullable=False),
        sa.Column("payment_token_address", sa.String(256), nullable=False),
        sa.Column("payment_amount", sa.Numeric, nullable=False),
        sa.Column("collection_address", sa.String(256), nullable=False),
        sa.Column("token_id", sa.Numeric, nullable=False),
        sa.PrimaryKeyConstraint("transaction_hash", "trace_address"),
    )


def downgrade():
    op.drop_table("nft_trades")
