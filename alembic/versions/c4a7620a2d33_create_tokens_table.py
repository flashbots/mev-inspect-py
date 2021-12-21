"""Create tokens table

Revision ID: c4a7620a2d33
Revises: 15ba9c27ee8a
Create Date: 2021-12-21 19:12:33.940117

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c4a7620a2d33"
down_revision = "15ba9c27ee8a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "tokens",
        sa.Column("token_address", sa.String(256), nullable=False),
        sa.Column("decimals", sa.Numeric, nullable=False),
        sa.PrimaryKeyConstraint("token_address"),
    )


def downgrade():
    op.drop_table("tokens")
