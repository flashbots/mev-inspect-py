"""empty message

Revision ID: 52d75a7e0533
Revises: 7cf0eeb41da0
Create Date: 2021-11-26 20:35:58.954138

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "52d75a7e0533"
down_revision = "7cf0eeb41da0"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "punk_bid_acceptances",
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("block_number", sa.Numeric, nullable=False),
        sa.Column("transaction_hash", sa.String(66), nullable=False),
        sa.Column("trace_address", sa.String(256), nullable=False),
        sa.Column("from_address", sa.String(256), nullable=False),
        sa.Column("punk_index", sa.Numeric, nullable=False),
        sa.Column("min_price", sa.Numeric, nullable=False),
        sa.PrimaryKeyConstraint("block_number", "transaction_hash", "trace_address"),
    )


def downgrade():
    op.drop_table("punk_bid_acceptances")
