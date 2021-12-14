"""Change classified traces primary key to include block number

Revision ID: a10d68643476
Revises: 3417f49d97b3
Create Date: 2021-11-02 22:03:26.312317

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "a10d68643476"
down_revision = "3417f49d97b3"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE classified_traces DROP CONSTRAINT classified_traces_pkey")
    op.create_primary_key(
        "classified_traces_pkey",
        "classified_traces",
        ["block_number", "transaction_hash", "trace_address"],
    )
    op.drop_index("i_block_number")


def downgrade():
    op.execute("ALTER TABLE classified_traces DROP CONSTRAINT classified_traces_pkey")
    op.create_index("i_block_number", "classified_traces", ["block_number"])
    op.create_primary_key(
        "classified_traces_pkey",
        "classified_traces",
        ["transaction_hash", "trace_address"],
    )
