"""empty message

Revision ID: 7cf0eeb41da0
Revises: d498bdb0a641
Create Date: 2021-11-26 20:27:28.936516

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "7cf0eeb41da0"
down_revision = "d498bdb0a641"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "punk_bids",
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("block_number", sa.Numeric, nullable=False),
        sa.Column("transaction_hash", sa.String(66), nullable=False),
        sa.Column("trace_address", sa.String(256), nullable=False),
        sa.Column("from_address", sa.String(256), nullable=False),
        sa.Column("punk_index", sa.Numeric, nullable=False),
        sa.Column("price", sa.Numeric, nullable=False),
        sa.PrimaryKeyConstraint("block_number", "transaction_hash", "trace_address"),
    )


def downgrade():
    op.drop_table("punk_bids")
