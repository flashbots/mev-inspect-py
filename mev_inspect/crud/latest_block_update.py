from typing import Optional


def find_latest_block_update(db_session) -> Optional[int]:
    result1 = db_session.execute(
        "SELECT block_number FROM swaps order by block_number desc LIMIT 1"
    ).one_or_none()
    result2 = db_session.execute(
        "SELECT block_number FROM liquidations order by block_number desc LIMIT 1"
    ).one_or_none()

    if result1 is None or result2 is None:
        return None
    else:
        return max(int(result1[0]), int(result2[0]))


def update_latest_block(db_session, block_number) -> None:
    db_session.execute(
        """
            UPDATE latest_block_update
                SET block_number = :block_number, updated_at = current_timestamp;
            INSERT INTO latest_block_update
                (block_number, updated_at)
            SELECT :block_number, current_timestamp
                WHERE NOT EXISTS (SELECT 1 FROM latest_block_update);
            """,
        params={"block_number": block_number},
    )
