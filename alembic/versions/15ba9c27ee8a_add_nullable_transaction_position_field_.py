"""Add nullable transaction_position field to swaps and traces

Revision ID: 15ba9c27ee8a
Revises: 04b76ab1d2af
Create Date: 2021-12-02 18:24:18.218880

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "15ba9c27ee8a"
down_revision = "ead7eb8283b9"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "classified_traces",
        sa.Column("transaction_position", sa.Numeric, nullable=True),
    )
    op.add_column("swaps", sa.Column("transaction_position", sa.Numeric, nullable=True))


def downgrade():
    op.drop_column("classified_traces", "transaction_position")
    op.drop_column("swaps", "transaction_position")
