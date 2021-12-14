"""Add to_address and from_address to miner_payments table

Revision ID: d70c08b4db6f
Revises: 083978d6e455
Create Date: 2021-08-30 22:10:04.186251

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d70c08b4db6f"
down_revision = "083978d6e455"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "miner_payments",
        sa.Column("transaction_to_address", sa.String(256), nullable=True),
    )
    op.add_column(
        "miner_payments",
        sa.Column("transaction_from_address", sa.String(256), nullable=True),
    )


def downgrade():
    op.drop_column("miner_payments", "transaction_to_address")
    op.drop_column("miner_payments", "transaction_from_address")
