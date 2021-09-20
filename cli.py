import os

import click
from web3 import Web3

from mev_inspect.db import get_session
from mev_inspect.inspect_block import inspect_block
from mev_inspect.provider import get_base_provider


RPC_URL_ENV = "RPC_URL"


@click.group()
def cli():
    pass


@cli.command()
@click.argument("block_number", type=int)
@click.option("--rpc", default=lambda: os.environ.get(RPC_URL_ENV, ""))
@click.option("--cache/--no-cache", default=True)
def inspect_block_command(block_number: int, rpc: str, cache: bool):
    db_session = get_session()
    base_provider = get_base_provider(rpc)
    w3 = Web3(base_provider)

    if not cache:
        click.echo("Skipping cache")

    inspect_block(db_session, base_provider, w3, block_number, should_cache=cache)


@cli.command()
@click.argument("after_block", type=int)
@click.argument("before_block", type=int)
@click.option("--rpc", default=lambda: os.environ.get(RPC_URL_ENV, ""))
@click.option("--cache/--no-cache", default=True)
def inspect_many_blocks_command(
    after_block: int, before_block: int, rpc: str, cache: bool
):

    db_session = get_session()
    base_provider = get_base_provider(rpc)
    w3 = Web3(base_provider)

    if not cache:
        click.echo("Skipping cache")

    for i, block_number in enumerate(range(after_block, before_block)):
        block_message = (
            f"Running for {block_number} ({i+1}/{before_block - after_block})"
        )
        dashes = "-" * len(block_message)
        click.echo(dashes)
        click.echo(block_message)
        click.echo(dashes)

        inspect_block(
            db_session,
            base_provider,
            w3,
            block_number,
            should_write_classified_traces=False,
            should_cache=cache,
        )


def get_rpc_url() -> str:
    return os.environ["RPC_URL"]


if __name__ == "__main__":
    cli()
