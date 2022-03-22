import itertools
import json
import logging
import os
from typing import Iterator, Optional, Tuple, TypeVar

import boto3

from mev_inspect.text_io import BytesIteratorIO

AWS_ENDPOINT_URL_ENV = "AWS_ENDPOINT_URL"
EXPORT_BUCKET_NAME_ENV = "EXPORT_BUCKET_NAME"
EXPORT_BUCKET_REGION_ENV = "EXPORT_BUCKET_REGION"
EXPORT_AWS_ACCESS_KEY_ID_ENV = "EXPORT_AWS_ACCESS_KEY_ID"
EXPORT_AWS_SECRET_ACCESS_KEY_ENV = "EXPORT_AWS_SECRET_ACCESS_KEY"

supported_tables = [
    "mev_summary",
    "arbitrages",
    "liquidations",
    "sandwiches",
    "sandwiched_swaps",
    "blocks",
]

logger = logging.getLogger(__name__)


def export_block(inspect_db_session, block_number: int) -> None:
    for table in supported_tables:
        _export_block_by_table(inspect_db_session, block_number, table)


def _export_block_by_table(inspect_db_session, block_number: int, table: str) -> None:
    client = get_s3_client()
    export_bucket_name = get_export_bucket_name()
    export_statement = _get_export_statement(table)

    object_key = f"{table}/flashbots_{block_number}.json"

    mev_summary_json_results = inspect_db_session.execute(
        statement=export_statement,
        params={
            "block_number": block_number,
        },
    )

    first_value, mev_summary_json_results = _peek(mev_summary_json_results)
    if first_value is None:
        existing_object_size = _get_object_size(client, export_bucket_name, object_key)
        if existing_object_size is None or existing_object_size == 0:
            logger.info(f"Skipping {table} for block {block_number} - no data")
            client.delete_object(
                Bucket=export_bucket_name,
                Key=object_key,
            )
            return

    mev_summary_json_fileobj = BytesIteratorIO(
        (f"{json.dumps(row)}\n".encode("utf-8") for (row,) in mev_summary_json_results)
    )

    client.delete_object(
        Bucket=export_bucket_name,
        Key=object_key,
    )

    client.upload_fileobj(
        mev_summary_json_fileobj,
        Bucket=export_bucket_name,
        Key=object_key,
    )

    logger.info(f"Exported to {object_key}")


def _get_export_statement(table: str) -> str:
    return f"""
        SELECT to_json(json)
        FROM (
            SELECT *, CURRENT_TIMESTAMP(0) as timestamp
            FROM {table}

        ) json
        WHERE
        block_number = :block_number
        """


def _get_object_size(client, bucket: str, key: str) -> Optional[int]:
    response = client.list_objects_v2(
        Bucket=bucket,
        Prefix=key,
    )

    for obj in response.get("Contents", []):
        if obj["Key"] == key:
            return obj["Size"]

    return None


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


_T = TypeVar("_T")


def _peek(iterable: Iterator[_T]) -> Tuple[Optional[_T], Iterator[_T]]:
    try:
        first = next(iterable)
    except StopIteration:
        return None, iter([])

    return first, itertools.chain([first], iterable)
