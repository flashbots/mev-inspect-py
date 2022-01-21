"""Add protocols column to arbitrages

Revision ID: bdbb545f6c03
Revises: bba80d21c5a4
Create Date: 2022-01-20 23:17:19.316008

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "bdbb545f6c03"
down_revision = "bba80d21c5a4"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "arbitrages",
        sa.Column("protocols", sa.ARRAY(sa.String(256)), server_default="{}"),
    )


def downgrade():
    op.drop_column("arbitrages", "protocols")
