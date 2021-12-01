from datetime import datetime

from mev_inspect.schemas.blocks import Block


def delete_block(
    db_session,
    block_number: int,
) -> None:
    db_session.execute(
        "DELETE FROM blocks WHERE block_number = :block_number",
        params={"block_number": block_number},
    )
    db_session.commit()


def write_block(
    db_session,
    block: Block,
) -> None:
    db_session.execute(
        "INSERT INTO blocks (block_number, block_timestamp) VALUES (:block_number, :block_timestamp)",
        params={
            "block_number": block.block_number,
            "block_timestamp": datetime.fromtimestamp(block.block_timestamp),
        },
    )
    db_session.commit()
