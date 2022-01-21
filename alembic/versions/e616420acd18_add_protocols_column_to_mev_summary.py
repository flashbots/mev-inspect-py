"""Add protocols column to mev_summary

Revision ID: e616420acd18
Revises: bdbb545f6c03
Create Date: 2022-01-21 00:11:51.516459

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e616420acd18"
down_revision = "bdbb545f6c03"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "mev_summary",
        sa.Column("protocols", sa.ARRAY(sa.String(256)), server_default="{}"),
    )


def downgrade():
    op.drop_column("mev_summary", "protocols")
