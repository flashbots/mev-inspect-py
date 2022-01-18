"""add profit_amount column to sandwiches table

Revision ID: b26ab0051a88
Revises: 3c54832385e3
Create Date: 2022-01-16 13:45:10.190969

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b26ab0051a88"
down_revision = "3c54832385e3"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "sandwiches", sa.Column("profit_token_address", sa.String(256), nullable=True)
    )
    op.add_column("sandwiches", sa.Column("profit_amount", sa.Numeric, nullable=True))


def downgrade():
    op.drop_column("sandwiches", "profit_token_address")
    op.drop_column("sandwiches", "profit_amount")
