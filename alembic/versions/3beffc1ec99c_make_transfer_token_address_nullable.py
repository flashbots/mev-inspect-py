"""Make transfer and swap token addresses nullable

Revision ID: 3beffc1ec99c
Revises: c8363617aa07
Create Date: 2021-10-08 16:27:52.058695

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "3beffc1ec99c"
down_revision = "c8363617aa07"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("transfers", "token_address", nullable=True)
    op.alter_column("swaps", "token_in_address", nullable=True)
    op.alter_column("swaps", "token_out_address", nullable=True)


def downgrade():
    op.alter_column("transfers", "token_address", nullable=False)
    op.alter_column("swaps", "token_in_address", nullable=False)
    op.alter_column("swaps", "token_out_address", nullable=False)
