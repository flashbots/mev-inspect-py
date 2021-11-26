"""Change blocks.timestamp to timestamp

Revision ID: 04b76ab1d2af
Revises: 2c90b2b8a80b
Create Date: 2021-11-26 15:31:21.111693

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "04b76ab1d2af"
down_revision = "0cef835f7b36"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "blocks",
        "block_timestamp",
        type_=sa.TIMESTAMP,
        nullable=False,
        postgresql_using="TO_TIMESTAMP(block_timestamp)",
    )


def downgrade():
    op.alter_column(
        "blocks",
        "block_timestamp",
        type_=sa.Numeric,
        nullable=False,
        postgresql_using="extract(epoch FROM block_timestamp)",
    )
