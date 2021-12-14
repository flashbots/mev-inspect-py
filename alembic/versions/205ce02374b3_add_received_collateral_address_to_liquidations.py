"""Add received_collateral_address to liquidations

Revision ID: 205ce02374b3
Revises: c8363617aa07
Create Date: 2021-10-04 19:52:40.017084

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "205ce02374b3"
down_revision = "c8363617aa07"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "liquidations",
        sa.Column("received_token_address", sa.String(256), nullable=True),
    )


def downgrade():
    op.drop_column("liquidations", "received_token_address")
