"""Create latest block table

Revision ID: a02f3f2c469f
Revises: d70c08b4db6f
Create Date: 2021-09-13 21:32:27.181344

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a02f3f2c469f"
down_revision = "d70c08b4db6f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "latest_block_update",
        sa.Column("block_number", sa.Numeric, primary_key=True),
        sa.Column("updated_at", sa.TIMESTAMP, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("latest_block_update")
