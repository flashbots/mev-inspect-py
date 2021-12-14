"""Add arbitrages and swap join table

Revision ID: 9d8c69b3dccb
Revises: 2116e2f36a19
Create Date: 2021-08-05 21:46:35.209199

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9d8c69b3dccb"
down_revision = "2116e2f36a19"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "arbitrages",
        sa.Column("id", sa.String(256), primary_key=True),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("account_address", sa.String(256), nullable=False),
        sa.Column("profit_token_address", sa.String(256), nullable=False),
        sa.Column("block_number", sa.Numeric, nullable=False),
        sa.Column("transaction_hash", sa.String(256), nullable=False),
        sa.Column("start_amount", sa.Numeric, nullable=False),
        sa.Column("end_amount", sa.Numeric, nullable=False),
        sa.Column("profit_amount", sa.Numeric, nullable=False),
    )


def downgrade():
    op.drop_table("arbitrages")
