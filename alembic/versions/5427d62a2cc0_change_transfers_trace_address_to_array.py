"""Change transfers trace address to ARRAY

Revision ID: 5427d62a2cc0
Revises: d540242ae368
Create Date: 2021-11-19 13:25:11.252774

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5427d62a2cc0"
down_revision = "d540242ae368"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("transfers_pkey", "transfers")
    op.alter_column(
        "transfers",
        "trace_address",
        type_=sa.ARRAY(sa.Integer),
        nullable=False,
        postgresql_using="trace_address::int[]",
    )
    op.create_primary_key(
        "transfers_pkey",
        "transfers",
        ["block_number", "transaction_hash", "trace_address"],
    )


def downgrade():
    op.drop_constraint("transfers_pkey", "transfers")
    op.alter_column(
        "transfers",
        "trace_address",
        type_=sa.String(256),
        nullable=False,
    )
    op.create_primary_key(
        "transfers_pkey",
        "transfers",
        ["block_number", "transaction_hash", "trace_address"],
    )
