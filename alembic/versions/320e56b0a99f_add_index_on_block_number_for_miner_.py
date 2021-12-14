"""Add index on block_number for miner_payments

Revision ID: 320e56b0a99f
Revises: a02f3f2c469f
Create Date: 2021-09-14 11:11:41.559137

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "320e56b0a99f"
down_revision = "a02f3f2c469f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("ix_block_number", "miner_payments", ["block_number"])


def downgrade():
    op.drop_index("ix_block_number", "miner_payments")
