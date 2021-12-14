"""Add error column to swaps

Revision ID: 92f28a2b4f52
Revises: 9b8ae51c5d56
Create Date: 2021-08-17 03:46:21.498821

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "92f28a2b4f52"
down_revision = "9b8ae51c5d56"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("swaps", sa.Column("error", sa.String(256), nullable=True))


def downgrade():
    op.drop_column("swaps", "error")
