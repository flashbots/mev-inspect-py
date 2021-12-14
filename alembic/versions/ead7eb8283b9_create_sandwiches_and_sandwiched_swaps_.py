"""Create sandwiches and sandwiched swaps tables

Revision ID: ead7eb8283b9
Revises: a5d80460f0e6
Create Date: 2021-12-03 16:37:28.077158

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ead7eb8283b9"
down_revision = "52d75a7e0533"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "sandwiches",
        sa.Column("id", sa.String(256), primary_key=True),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("block_number", sa.Numeric, nullable=False),
        sa.Column("sandwicher_address", sa.String(256), nullable=False),
        sa.Column("frontrun_swap_transaction_hash", sa.String(256), nullable=False),
        sa.Column("frontrun_swap_trace_address", sa.ARRAY(sa.Integer), nullable=False),
        sa.Column("backrun_swap_transaction_hash", sa.String(256), nullable=False),
        sa.Column("backrun_swap_trace_address", sa.ARRAY(sa.Integer), nullable=False),
    )

    op.create_index(
        "ik_sandwiches_frontrun",
        "sandwiches",
        [
            "block_number",
            "frontrun_swap_transaction_hash",
            "frontrun_swap_trace_address",
        ],
    )

    op.create_index(
        "ik_sandwiches_backrun",
        "sandwiches",
        ["block_number", "backrun_swap_transaction_hash", "backrun_swap_trace_address"],
    )

    op.create_table(
        "sandwiched_swaps",
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("sandwich_id", sa.String(1024), primary_key=True),
        sa.Column("block_number", sa.Numeric, primary_key=True),
        sa.Column("transaction_hash", sa.String(66), primary_key=True),
        sa.Column("trace_address", sa.ARRAY(sa.Integer), primary_key=True),
        sa.ForeignKeyConstraint(["sandwich_id"], ["sandwiches.id"], ondelete="CASCADE"),
    )

    op.create_index(
        "ik_sandwiched_swaps_secondary",
        "sandwiched_swaps",
        ["block_number", "transaction_hash", "trace_address"],
    )


def downgrade():
    op.drop_index("ik_sandwiched_swaps_secondary")
    op.drop_table("sandwiched_swaps")
    op.drop_index("ik_sandwiches_frontrun")
    op.drop_index("ik_sandwiches_backrun")
    op.drop_table("sandwiches")
