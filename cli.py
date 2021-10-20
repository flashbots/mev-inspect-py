import asyncio
import logging
import os
import sys
from functools import wraps

import click
from web3 import Web3
from web3.eth import AsyncEth

from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.db import get_inspect_session, get_trace_session
from mev_inspect.inspect_block import inspect_block
from mev_inspect.provider import get_base_provider
from mev_inspect.retry import http_retry_with_backoff_request_middleware

RPC_URL_ENV = "RPC_URL"

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

semaphore: asyncio.Semaphore


@click.group()
def cli():
    pass


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(f(*args, **kwargs))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    return wrapper


@cli.command()
@click.argument("block_number", type=int)
@click.option("--rpc", default=lambda: os.environ.get(RPC_URL_ENV, ""))
@click.option("--cache/--no-cache", default=True)
@coro
async def inspect_block_command(block_number: int, rpc: str, cache: bool):
    inspect_db_session = get_inspect_session()
    trace_db_session = get_trace_session()

    base_provider = get_base_provider(rpc)
    w3 = Web3(base_provider, modules={"eth": (AsyncEth,)}, middlewares=[])
    trace_classifier = TraceClassifier()

    if not cache:
        logger.info("Skipping cache")

    await inspect_block(
        inspect_db_session,
        base_provider,
        w3,
        trace_classifier,
        block_number,
        trace_db_session=trace_db_session,
    )


@cli.command()
@click.argument("after_block", type=int)
@click.argument("before_block", type=int)
@click.option("--rpc", default=lambda: os.environ.get(RPC_URL_ENV, ""))
@click.option("--cache/--no-cache", default=True)
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
    cache: bool,
    max_concurrency: int,
    request_timeout: int,
):
    global semaphore  # pylint: disable=global-statement
    semaphore = asyncio.Semaphore(max_concurrency)
    inspect_db_session = get_inspect_session()
    trace_db_session = get_trace_session()

    base_provider = get_base_provider(rpc, request_timeout=request_timeout)
    w3 = Web3(
        base_provider,
        modules={"eth": (AsyncEth,)},
        middlewares=[http_retry_with_backoff_request_middleware],
    )

    trace_classifier = TraceClassifier()

    if not cache:
        logger.info("Skipping cache")

    tasks = []

    for block_number in range(after_block, before_block):
        tasks.append(
            asyncio.ensure_future(
                safe_inspect_block(
                    inspect_db_session,
                    base_provider,
                    w3,
                    trace_classifier,
                    block_number,
                    trace_db_session,
                )
            )
        )
    logger.info(f"Gathered {len(tasks)} blocks to inspect")
    await asyncio.gather(*tasks)


async def safe_inspect_block(
    inspect_db_session,
    base_provider,
    w3,
    trace_classifier,
    block_number,
    trace_db_session,
):
    async with semaphore:
        return await inspect_block(
            inspect_db_session,
            base_provider,
            w3,
            trace_classifier,
            block_number,
            trace_db_session=trace_db_session,
        )


def get_rpc_url() -> str:
    return os.environ["RPC_URL"]


if __name__ == "__main__":
    cli()
