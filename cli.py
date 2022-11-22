import fileinput
import logging
import os
import sys
from datetime import datetime

import click
import dramatiq

from mev_inspect.concurrency import coro
from mev_inspect.crud.prices import write_prices
from mev_inspect.db import get_inspect_session, get_trace_session
from mev_inspect.inspector import MEVInspector
from mev_inspect.prices import fetch_prices, fetch_prices_range
from mev_inspect.queue.broker import connect_broker
from mev_inspect.queue.tasks import (
    LOW_PRIORITY,
    LOW_PRIORITY_QUEUE,
    backfill_export_task,
    inspect_many_blocks_task,
)
from mev_inspect.s3_export import export_block

RPC_URL_ENV = "RPC_URL"

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("block_number", type=int)
@click.option("--rpc", default=lambda: os.environ.get(RPC_URL_ENV, ""))
@coro
async def inspect_block_command(block_number: int, rpc: str):
    inspect_db_session = get_inspect_session()
    trace_db_session = get_trace_session()

    inspector = MEVInspector(rpc)

    await inspector.inspect_single_block(
        inspect_db_session=inspect_db_session,
        trace_db_session=trace_db_session,
        block=block_number,
    )


@cli.command()
@click.argument("block_number", type=int)
@click.option("--rpc", default=lambda: os.environ.get(RPC_URL_ENV, ""))
@coro
async def fetch_block_command(block_number: int, rpc: str):
    trace_db_session = get_trace_session()

    inspector = MEVInspector(rpc)
    block = await inspector.create_from_block(
        block_number=block_number,
        trace_db_session=trace_db_session,
    )

    print(block.json())


@cli.command()
@click.argument("after_block", type=int)
@click.argument("before_block", type=int)
@click.option("--rpc", default=lambda: os.environ.get(RPC_URL_ENV, ""))
@click.option(
    "--max-concurrency",
    type=int,
    help="maximum number of concurrent connections",
    default=1,
)
@click.option(
    "--request-timeout", type=int, help="timeout for requests to nodes", default=500
)
@coro
async def inspect_many_blocks_command(
    after_block: int,
    before_block: int,
    rpc: str,
    max_concurrency: int,
    request_timeout: int,
):
    inspect_db_session = get_inspect_session()
    trace_db_session = get_trace_session()

    inspector = MEVInspector(
        rpc,
        max_concurrency=max_concurrency,
        request_timeout=request_timeout,
    )
    await inspector.inspect_many_blocks(
        inspect_db_session=inspect_db_session,
        trace_db_session=trace_db_session,
        after_block=after_block,
        before_block=before_block,
    )


@cli.command()
def enqueue_block_list_command():
    broker = connect_broker()
    inspect_many_blocks_actor = dramatiq.actor(
        inspect_many_blocks_task,
        broker=broker,
        queue_name=LOW_PRIORITY_QUEUE,
        priority=LOW_PRIORITY,
    )

    for block_string in fileinput.input():
        block = int(block_string)
        logger.info(f"Sending {block} to {block+1}")
        inspect_many_blocks_actor.send(block, block + 1)


@cli.command()
@click.argument("start_block", type=int)
@click.argument("end_block", type=int)
@click.argument("batch_size", type=int, default=10)
def enqueue_many_blocks_command(start_block: int, end_block: int, batch_size: int):
    broker = connect_broker()
    inspect_many_blocks_actor = dramatiq.actor(
        inspect_many_blocks_task,
        broker=broker,
        queue_name=LOW_PRIORITY_QUEUE,
        priority=LOW_PRIORITY,
    )

    if start_block < end_block:
        after_block = start_block
        before_block = end_block

        for batch_after_block in range(after_block, before_block, batch_size):
            batch_before_block = min(batch_after_block + batch_size, before_block)
            logger.info(f"Sending {batch_after_block} to {batch_before_block}")
            inspect_many_blocks_actor.send(batch_after_block, batch_before_block)
    else:
        after_block = end_block
        before_block = start_block

        for batch_before_block in range(before_block, after_block, -1 * batch_size):
            batch_after_block = max(batch_before_block - batch_size, after_block)
            logger.info(f"Sending {batch_after_block} to {batch_before_block}")
            inspect_many_blocks_actor.send(batch_after_block, batch_before_block)


@cli.command()
def fetch_all_prices():
    inspect_db_session = get_inspect_session()

    logger.info("Fetching prices")
    prices = fetch_prices()

    logger.info("Writing prices")
    write_prices(inspect_db_session, prices)


@cli.command()
@click.argument("block_number", type=int)
def enqueue_s3_export(block_number: int):
    broker = connect_broker()
    export_actor = dramatiq.actor(
        backfill_export_task,
        broker=broker,
        queue_name=LOW_PRIORITY_QUEUE,
        priority=LOW_PRIORITY,
    )
    logger.info(f"Sending block {block_number} export to queue")
    export_actor.send(block_number)


@cli.command()
@click.argument("after_block", type=int)
@click.argument("before_block", type=int)
def enqueue_many_s3_exports(after_block: int, before_block: int):
    broker = connect_broker()
    export_actor = dramatiq.actor(
        backfill_export_task,
        broker=broker,
        queue_name=LOW_PRIORITY_QUEUE,
        priority=LOW_PRIORITY,
    )
    logger.info(f"Sending blocks {after_block} to {before_block} to queue")
    for block_number in range(after_block, before_block):
        export_actor.send(block_number)


@cli.command()
@click.argument("block_number", type=int)
def s3_export(block_number: int):
    inspect_db_session = get_inspect_session()
    logger.info(f"Exporting {block_number}")
    export_block(inspect_db_session, block_number)


@cli.command()
@click.argument("after", type=click.DateTime(formats=["%Y-%m-%d", "%m-%d-%Y"]))
@click.argument("before", type=click.DateTime(formats=["%Y-%m-%d", "%m-%d-%Y"]))
def fetch_range(after: datetime, before: datetime):
    inspect_db_session = get_inspect_session()

    logger.info("Fetching prices")
    prices = fetch_prices_range(after, before)

    logger.info("Writing prices")
    write_prices(inspect_db_session, prices)


def get_rpc_url() -> str:
    return os.environ["RPC_URL"]


if __name__ == "__main__":
    cli()
