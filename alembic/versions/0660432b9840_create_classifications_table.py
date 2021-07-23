"""Create classifications table

Revision ID: 0660432b9840
Revises: 
Create Date: 2021-07-23 20:08:42.016711

"""
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON
from alembic import op

# revision identifiers, used by Alembic.
revision = "0660432b9840"
down_revision = None
branch_labels = None
depends_on = None

CLASSIFICATION_TYPES = [
    "unknown",
]

TRACE_TYPES = [
    "call",
    "create",
    "delegateCall",
    "reward",
    "suicide",
]

PROTOCOL_TYPES = [
    "uniswap_v2",
]


def upgrade():
    op.create_table(
        "classifications",
        sa.Column("classified_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("transaction_hash", sa.String(66), nullable=False),
        sa.Column("block_number", sa.Integer, nullable=False),
        sa.Column(
            "classification_type",
            sa.Enum(*CLASSIFICATION_TYPES, name="classification_type"),
            nullable=False,
        ),
        sa.Column(
            "trace_type", sa.Enum(*TRACE_TYPES, name="trace_type"), nullable=False
        ),
        sa.Column("trace_address", sa.String(256), nullable=False),
        sa.Column("protocol", sa.Enum(*PROTOCOL_TYPES, name="protocol"), nullable=True),
        sa.Column("function_name", sa.String(2048), nullable=True),
        sa.Column("function_signature", sa.String(2048), nullable=True),
        sa.Column("input", JSON, nullable=True),
        sa.Column("from_address", sa.String(256), nullable=True),
        sa.Column("to_address", sa.String(256), nullable=True),
        sa.Column("value", sa.Integer, nullable=True),
        sa.PrimaryKeyConstraint("transaction_hash"),
    )


def downgrade():
    op.drop_table("classifications")
    sa.Enum(name="trace_type").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="classification_type").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="protocol").drop(op.get_bind(), checkfirst=False)
