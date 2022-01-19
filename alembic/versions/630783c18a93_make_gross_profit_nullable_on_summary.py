"""Make gross profit nullable on summary

Revision ID: 630783c18a93
Revises: ab9a9e449ff9
Create Date: 2022-01-19 23:09:51.816948

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "630783c18a93"
down_revision = "ab9a9e449ff9"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("mev_summary", "gross_profit_usd", nullable=True)


def downgrade():
    op.alter_column("mev_summary", "gross_profit_usd", nullable=False)
