import json

import boto3

from mev_inspect.text_io import BytesIteratorIO

MEV_SUMMARY_EXPORT_QUERY = """
    SELECT to_json(mev_summary)
    FROM mev_summary 
    WHERE
        block_number >= :after_block_number AND
        block_number < :before_block_number
    """


def export_block_range(
    inspect_db_session, after_block_number: int, before_block_number
) -> None:
    client = get_s3_client()
    bucket_name = get_export_bucket_name()

    mev_summary_json_results = inspect_db_session.execute(
        statement=MEV_SUMMARY_EXPORT_QUERY,
        params={
            "after_block_number": after_block_number,
            "before_block_number": before_block_number,
        },
    )

    mev_summary_json_fileobj = BytesIteratorIO(
        (f"{json.dumps(row)}\n".encode("utf-8") for (row,) in mev_summary_json_results)
    )

    key = f"mev_summary/{after_block_number}-{before_block_number}.json"

    client.upload_fileobj(
        mev_summary_json_fileobj,
        Bucket=bucket_name,
        Key=key,
    )


def list_export_bucket():
    client = get_s3_client()
    return client.list_objects_v2(
        Bucket=get_export_bucket_name(),
        Prefix="/",
    )


# TODO - replaced by ConfigMap
def get_export_bucket_name() -> str:
    return "local-export"


# TODO
def get_s3_client():
    return boto3.client(
        "s3",
        region_name="us-east-1",
        endpoint_url="http://localstack:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
