"""Add index for classified_traces.block_number

Revision ID: c5da44eb072c
Revises: 0660432b9840
Create Date: 2021-07-30 17:37:27.335475

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "c5da44eb072c"
down_revision = "0660432b9840"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("i_block_number", "classified_traces", ["block_number"])


def downgrade():
    op.drop_index("i_block_number", "classified_traces")
