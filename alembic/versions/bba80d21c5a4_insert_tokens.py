"""Add tokens to database

Revision ID: bba80d21c5a4
Revises: b26ab0051a88
Create Date: 2022-01-19 22:19:59.514998

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "bba80d21c5a4"
down_revision = "630783c18a93"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        INSERT INTO tokens (token_address,decimals) VALUES
        ('0x514910771af9ca656af840dff83e8264ecf986ca',18),
        ('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',18),
        ('0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',18),
        ('0x0bc529c00c6401aef6d220be8c6ea1667f6ad93e',18),
        ('0x5d3a536e4d6dbd6114cc1ead35777bab948e3643',8),
        ('0x2260fac5e5542a773aa44fbcfedf7c193bc2c599',8),
        ('0x80fb784b7ed66730e8b1dbd9820afd29931aab03',18),
        ('0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5',8),
        ('0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',6),
        ('0xdac17f958d2ee523a2206206994597c13d831ec7',6),
        ('0x6b175474e89094c44da98b954eedeac495271d0f',18),
        ('0x0000000000085d4780b73119b644ae5ecd22b376',18),
        ('0x39aa39c021dfbae8fac545936693ac917d5e7563',8),
        ('0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9',18);
        """
    )


def downgrade():
    op.execute("DELETE FROM tokens")
