import logging
import os
import sys

import click

from mev_inspect.concurrency import coro
from mev_inspect.db import get_inspect_session, get_trace_session
from mev_inspect.inspector import MEVInspector

RPC_URL_ENV = "RPC_URL"

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


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

    inspector = MEVInspector(rpc, inspect_db_session, trace_db_session)
    await inspector.inspect_single_block(block=block_number)


@cli.command()
@click.argument("block_number", type=int)
@click.option("--rpc", default=lambda: os.environ.get(RPC_URL_ENV, ""))
@coro
async def fetch_block_command(block_number: int, rpc: str):
    inspect_db_session = get_inspect_session()
    trace_db_session = get_trace_session()

    inspector = MEVInspector(rpc, inspect_db_session, trace_db_session)
    block = await inspector.create_from_block(block_number=block_number)
    print(block.json())


@cli.command()
@click.argument("after_block", type=int)
@click.argument("before_block", type=int)
@click.option("--rpc", default=lambda: os.environ.get(RPC_URL_ENV, ""))
@click.option(
    "--max-concurrency",
    type=int,
    help="maximum number of concurrent connections",
    default=5,
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
        inspect_db_session,
        trace_db_session,
        max_concurrency=max_concurrency,
        request_timeout=request_timeout,
    )
    await inspector.inspect_many_blocks(
        after_block=after_block, before_block=before_block
    )


def get_rpc_url() -> str:
    return os.environ["RPC_URL"]


if __name__ == "__main__":
    cli()
