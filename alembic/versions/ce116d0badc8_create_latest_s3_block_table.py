"""Create latest_s3_block table

Revision ID: ce116d0badc8
Revises: 5c5375de15fd
Create Date: 2022-01-31 23:36:34.971594

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ce116d0badc8"
down_revision = "5c5375de15fd"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "latest_s3_block",
        sa.Column("block_number", sa.Numeric, nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("latest_s3_block")
