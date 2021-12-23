"""Add error column to liquidations

Revision ID: 4b9d289f2d74
Revises: 99d376cb93cc
Create Date: 2021-12-23 14:54:28.406159

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4b9d289f2d74"
down_revision = "99d376cb93cc"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("liquidations", sa.Column("error", sa.String(256), nullable=True))


def downgrade():
    op.drop_column("liquidations", "error")
