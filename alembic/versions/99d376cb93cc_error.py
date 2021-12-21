"""error column

Revision ID: 99d376cb93cc
Revises: c4a7620a2d33
Create Date: 2021-12-21 21:26:12.142484

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "99d376cb93cc"
down_revision = "c4a7620a2d33"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("arbitrages", sa.Column("error", sa.String(256), nullable=True))


def downgrade():
    op.drop_column("arbitrages", "error")
