import asyncio
import os
import signal
from functools import wraps

import click

from mev_inspect.inspector import MEVInspector

RPC_URL_ENV = "RPC_URL"


@click.group()
def cli():
    pass


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()

        def cancel_task_callback():
            for task in asyncio.all_tasks():
                task.cancel()

        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, cancel_task_callback)
        try:
            loop.run_until_complete(f(*args, **kwargs))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())

    return wrapper


@cli.command()
@click.argument("block_number", type=int)
@click.option("--rpc", default=lambda: os.environ.get(RPC_URL_ENV, ""))
@click.option("--cache/--no-cache", default=True)
@coro
async def inspect_block_command(block_number: int, rpc: str, cache: bool):
    inspector = MEVInspector(rpc=rpc, cache=cache)
    await inspector.inspect_single_block(block=block_number)


@cli.command()
@click.argument("block_number", type=int)
@click.option("--rpc", default=lambda: os.environ.get(RPC_URL_ENV, ""))
@coro
async def fetch_block_command(block_number: int, rpc: str):
    inspector = MEVInspector(rpc=rpc)
    block = await inspector.create_from_block(block_number=block_number)
    print(block.json())


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
    inspector = MEVInspector(
        rpc=rpc,
        cache=cache,
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
