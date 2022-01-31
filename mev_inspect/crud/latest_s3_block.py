from typing import Optional


def find_latest_s3_block(db_session) -> Optional[int]:
    result = db_session.execute(
        "SELECT block_number FROM latest_s3_block LIMIT 1"
    ).one_or_none()
    if result is None:
        return None
    else:
        return int(result[0])


def update_latest_s3_block(db_session, block_number) -> None:
    db_session.execute(
        """
            UPDATE latest_s3_block
                SET block_number = :block_number, updated_at = current_timestamp;
            INSERT INTO latest_s3_block
                (block_number, updated_at)
            SELECT :block_number, current_timestamp
                WHERE NOT EXISTS (SELECT 1 FROM latest_s3_blocks);
            """,
        params={"block_number": block_number},
    )
