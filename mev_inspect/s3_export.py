import json
import logging
import os
from typing import Optional

import boto3

from mev_inspect.text_io import BytesIteratorIO

AWS_ENDPOINT_URL_ENV = "AWS_ENDPOINT_URL"
EXPORT_BUCKET_NAME_ENV = "EXPORT_BUCKET_NAME"
EXPORT_BUCKET_REGION_ENV = "EXPORT_BUCKET_REGION"
EXPORT_AWS_ACCESS_KEY_ID_ENV = "EXPORT_AWS_ACCESS_KEY_ID"
EXPORT_AWS_SECRET_ACCESS_KEY_ENV = "EXPORT_AWS_SECRET_ACCESS_KEY"

MEV_SUMMARY_EXPORT_QUERY = """
    SELECT to_json(mev_summary)
    FROM mev_summary
    WHERE
        block_number >= :after_block_number AND
        block_number < :before_block_number
    """

logger = logging.getLogger(__name__)


def export_block_range(
    inspect_db_session, after_block_number: int, before_block_number
) -> None:
    export_bucket_name = get_export_bucket_name()
    client = get_s3_client()

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

    key = f"mev_summary/flashbots_{after_block_number}_{before_block_number}.json"

    client.upload_fileobj(
        mev_summary_json_fileobj,
        Bucket=export_bucket_name,
        Key=key,
    )

    logger.info(f"Exported to {key}")


def get_s3_client():
    endpoint_url = get_endpoint_url()
    return boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        region_name=get_export_bucket_region(),
        aws_access_key_id=get_export_aws_access_key_id(),
        aws_secret_access_key=get_export_aws_secret_access_key(),
    )


def get_endpoint_url() -> Optional[str]:
    return os.environ.get(AWS_ENDPOINT_URL_ENV)


def get_export_bucket_name() -> str:
    return os.environ[EXPORT_BUCKET_NAME_ENV]


def get_export_bucket_region() -> Optional[str]:
    return os.environ.get(EXPORT_BUCKET_REGION_ENV)


def get_export_aws_access_key_id() -> Optional[str]:
    return os.environ.get(EXPORT_AWS_ACCESS_KEY_ID_ENV)


def get_export_aws_secret_access_key() -> Optional[str]:
    return os.environ.get(EXPORT_AWS_SECRET_ACCESS_KEY_ENV)
