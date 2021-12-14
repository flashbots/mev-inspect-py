"""Create usd_prices table

Revision ID: d540242ae368
Revises: 2c90b2b8a80b
Create Date: 2021-11-18 04:30:06.802857

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d540242ae368"
down_revision = "2c90b2b8a80b"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "prices",
        sa.Column("timestamp", sa.TIMESTAMP),
        sa.Column("usd_price", sa.Numeric, nullable=False),
        sa.Column("token_address", sa.String(256), nullable=False),
        sa.PrimaryKeyConstraint("token_address", "timestamp"),
    )


def downgrade():
    op.drop_table("prices")
