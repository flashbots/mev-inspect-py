"""Create classifications table

Revision ID: 0660432b9840
Revises: 
Create Date: 2021-07-23 20:08:42.016711

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0660432b9840"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "classified_traces",
        sa.Column("classified_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("transaction_hash", sa.String(66), nullable=False),
        sa.Column("block_number", sa.Numeric, nullable=False),
        sa.Column(
            "classification",
            sa.String(256),
            nullable=False,
        ),
        sa.Column("trace_type", sa.String(256), nullable=False),
        sa.Column("trace_address", sa.String(256), nullable=False),
        sa.Column("protocol", sa.String(256), nullable=True),
        sa.Column("abi_name", sa.String(1024), nullable=True),
        sa.Column("function_name", sa.String(2048), nullable=True),
        sa.Column("function_signature", sa.String(2048), nullable=True),
        sa.Column("inputs", sa.JSON, nullable=True),
        sa.Column("from_address", sa.String(256), nullable=True),
        sa.Column("to_address", sa.String(256), nullable=True),
        sa.Column("gas", sa.Numeric, nullable=True),
        sa.Column("value", sa.Numeric, nullable=True),
        sa.Column("gas_used", sa.Numeric, nullable=True),
        sa.Column("error", sa.String(256), nullable=True),
        sa.PrimaryKeyConstraint("transaction_hash", "trace_address"),
    )


def downgrade():
    op.drop_table("classified_traces")
