"""Rename pool_address to contract_address

Revision ID: 0cef835f7b36
Revises: 5427d62a2cc0
Create Date: 2021-11-19 15:36:15.152622

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "0cef835f7b36"
down_revision = "5427d62a2cc0"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "swaps", "pool_address", nullable=False, new_column_name="contract_address"
    )


def downgrade():
    op.alter_column(
        "swaps", "contract_address", nullable=False, new_column_name="pool_address"
    )
