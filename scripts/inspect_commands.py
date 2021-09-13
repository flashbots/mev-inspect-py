import click
from web3 import Web3

from mev_inspect.db import get_session
from mev_inspect.inspect_block import inspect_block
from mev_inspect.retry import http_retry_with_backoff_request_middleware


@click.group()
def cli():
    pass


@cli.command()
@click.argument("block_number", type=int)
@click.argument("rpc")
@click.option("--cache/--no-cache", default=True)
def inspect_block_command(block_number: int, rpc: str, cache: bool):
    db_session = get_session()
    base_provider = _get_base_provider(rpc)
    w3 = Web3(base_provider)

    if not cache:
        click.echo("Skipping cache")

    inspect_block(db_session, base_provider, w3, block_number, should_cache=cache)


@cli.command()
@click.argument("after_block", type=int)
@click.argument("before_block", type=int)
@click.argument("rpc")
@click.option("--cache/--no-cache", default=True)
def inspect_many_blocks_command(
    after_block: int, before_block: int, rpc: str, cache: bool
):

    db_session = get_session()
    base_provider = _get_base_provider(rpc)
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


def _get_base_provider(rpc: str) -> Web3.HTTPProvider:
    base_provider = Web3.HTTPProvider(rpc)
    base_provider.middlewares.remove("http_retry_request")
    base_provider.middlewares.add(
        http_retry_with_backoff_request_middleware,
        "http_retry_with_backoff",
    )

    return base_provider


if __name__ == "__main__":
    cli()
