from mev_inspect.crud.latest_s3_block import (
    find_latest_s3_block,
    update_latest_s3_block,
)


def s3_export(
    db_session, block_number: int, bucket: str, filepath: str, region: str
) -> None:
    """Export block to S3"""

    uri = _get_uri(db_session, bucket, filepath, region)

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
    bucket: str,
    filepath_base: str,
    region: str,
) -> None:
    """Export block range to S3"""

    latest_s3_block = find_latest_s3_block(db_session)

    for block_number in range(after_block, before_block):
        if latest_s3_block is not None:
            if block_number > latest_s3_block:
                filepath = f"{filepath_base}" + f"{block_number}"
                uri = _get_uri(db_session, bucket, filepath, region)
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


def _get_uri(db_session, bucket: str, filepath: str, region: str) -> str:

    uri = db_session.execute(
        """
            SELECT aws_commons.create_s3_uri(
               '{bucket}',
               '{filepath}',
               '{region}'
            ) AS s3_uri_1 \gset
            """,
        params={"bucket": bucket, "filepath": filepath, "region": region},
    )

    return uri
