"""Remove collateral_token_address column

Revision ID: b9fa1ecc9929
Revises: 04b76ab1d2af
Create Date: 2021-12-01 23:32:40.574108

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "b9fa1ecc9929"
down_revision = "04b76ab1d2af"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("liquidations", "collateral_token_address")


def downgrade():
    op.add_column(
        "liquidations",
        sa.Column("collateral_token_address", sa.String(256), nullable=False),
    )
