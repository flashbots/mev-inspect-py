from mev_inspect.crud.latest_s3_block import (
    find_latest_s3_block,
    update_latest_s3_block,
)


def s3_export(
    db_session,
    block_number: int,
    uri: str,
) -> None:
    """Export block to S3"""

    latest_s3_block = find_latest_s3_block(db_session)

    if latest_s3_block is not None:

        if block_number > latest_s3_block:

            db_session.execute(
                """
                SELECT * FROM aws_s3.query_export_to_s3(
                    'SELECT *
            	     FROM mev_summary
            	     WHERE block_number={block_number}',
                     :{uri}
            """,
                params={"block_number": block_number, "uri": uri},
            )
            update_latest_s3_block(db_session, block_number)


def s3_export_many(
    db_session,
    after_block: int,
    before_block: int,
    uri: str,
) -> None:
    """Export block range to S3"""

    latest_s3_block = find_latest_s3_block(db_session)

    for block_number in range(after_block, before_block):

        if latest_s3_block is not None:

            if block_number > latest_s3_block:

                uri += f"/{block_number}"
                db_session.execute(
                    """
                    SELECT * FROM aws_s3.query_export_to_s3(
                        'SELECT *
                	     FROM mev_summary
                	     WHERE block_number={block_number}
                         :{uri}
                    """,
                    params={
                        "after_block": after_block,
                        "before_block": before_block,
                        "uri": uri,
                    },
                )
                update_latest_s3_block(db_session, block_number)
