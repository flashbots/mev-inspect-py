"""Change trace addresses to array types

Revision ID: 7eec417a4f3e
Revises: 9d8c69b3dccb
Create Date: 2021-08-06 15:58:04.556762

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7eec417a4f3e"
down_revision = "9d8c69b3dccb"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("swaps_pkey", "swaps")
    op.drop_column("swaps", "trace_address")
    op.add_column("swaps", sa.Column("trace_address", sa.ARRAY(sa.Integer)))
    op.create_primary_key("swaps_pkey", "swaps", ["transaction_hash", "trace_address"])

    op.drop_constraint("classified_traces_pkey", "classified_traces")
    op.drop_column("classified_traces", "trace_address")
    op.add_column("classified_traces", sa.Column("trace_address", sa.ARRAY(sa.Integer)))
    op.create_primary_key(
        "classified_traces_pkey",
        "classified_traces",
        ["transaction_hash", "trace_address"],
    )


def downgrade():
    op.drop_constraint("swaps_pkey", "swaps")
    op.drop_column("swaps", "trace_address")
    op.add_column("swaps", sa.Column("trace_address", sa.String))

    op.create_primary_key("swaps_pkey", "swaps", ["transaction_hash", "trace_address"])

    op.drop_constraint("classified_traces_pkey", "classified_traces")
    op.drop_column("classified_traces", "trace_address")
    op.add_column("classified_traces", sa.Column("trace_address", sa.String))

    op.create_primary_key(
        "classified_traces_pkey",
        "classified_traces",
        ["transaction_hash", "trace_address"],
    )
