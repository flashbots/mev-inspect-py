"""Add block timestamp to liquidations

Revision ID: f19270a53410
Revises: 52d75a7e0533
Create Date: 2021-12-14 02:40:46.802125

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "f19270a53410"
down_revision = "52d75a7e0533"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "liquidations", sa.Column("block_timestamp", sa.TIMESTAMP, nullable=True)
    )
    pass


def downgrade():
    sa.drop_column("block_timestamp", "liquidations")
    pass
