from mev_inspect.schemas.blocks import Block


async def delete_block(
    db_session,
    block_number: int,
) -> None:
    await db_session.execute(
        "DELETE FROM blocks WHERE block_number = :block_number",
        params={"block_number": block_number},
    )
    await db_session.commit()
    await db_session.flush()


async def write_block(
    db_session,
    block: Block,
) -> None:
    await db_session.execute(
        "INSERT INTO blocks (block_number, block_timestamp) VALUES (:block_number, :block_timestamp)",
        params={
            "block_number": block.block_number,
            "block_timestamp": block.block_timestamp,
        },
    )
    await db_session.commit()
    await db_session.flush()
