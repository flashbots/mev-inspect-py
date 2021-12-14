"""Create liquidations table

Revision ID: c8363617aa07
Revises: cd96af55108e
Create Date: 2021-09-29 14:00:06.857103

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c8363617aa07"
down_revision = "cd96af55108e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "liquidations",
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("liquidated_user", sa.String(256), nullable=False),
        sa.Column("liquidator_user", sa.String(256), nullable=False),
        sa.Column("collateral_token_address", sa.String(256), nullable=False),
        sa.Column("debt_token_address", sa.String(256), nullable=False),
        sa.Column("debt_purchase_amount", sa.Numeric, nullable=False),
        sa.Column("received_amount", sa.Numeric, nullable=False),
        sa.Column("protocol", sa.String(256), nullable=True),
        sa.Column("transaction_hash", sa.String(66), nullable=False),
        sa.Column("trace_address", sa.String(256), nullable=False),
        sa.Column("block_number", sa.Numeric, nullable=False),
        sa.PrimaryKeyConstraint("transaction_hash", "trace_address"),
    )


def downgrade():
    op.drop_table("liquidations")
