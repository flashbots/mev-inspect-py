"""Add blocks table

Revision ID: 2c90b2b8a80b
Revises: 04a3bb3740c3
Create Date: 2021-11-17 18:29:13.065944

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2c90b2b8a80b"
down_revision = "04a3bb3740c3"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "blocks",
        sa.Column("block_number", sa.Numeric, nullable=False),
        sa.Column("block_timestamp", sa.Numeric, nullable=False),
        sa.PrimaryKeyConstraint("block_number"),
    )


def downgrade():
    op.drop_table("blocks")
