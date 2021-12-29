from datetime import datetime
from typing import List

from mev_inspect.schemas.blocks import Block


def delete_blocks(
    db_session,
    after_block_number: int,
    before_block_number: int,
) -> None:
    db_session.execute(
        """
        DELETE FROM blocks
        WHERE
            block_number >= :after_block_number AND
            block_number < :before_block_number
        """,
        params={
            "after_block_number": after_block_number,
            "before_block_number": before_block_number,
        },
    )
    db_session.commit()


def write_blocks(
    db_session,
    blocks: List[Block],
) -> None:
    block_params = [
        {
            "block_number": block.block_number,
            "block_timestamp": datetime.fromtimestamp(block.block_timestamp),
        }
        for block in blocks
    ]

    db_session.execute(
        "INSERT INTO blocks (block_number, block_timestamp) VALUES (:block_number, :block_timestamp)",
        params=block_params,
    )
    db_session.commit()
