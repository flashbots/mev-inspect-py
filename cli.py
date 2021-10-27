import os
import logging
import sys

import click
from web3 import Web3

from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.db import get_inspect_session, get_trace_session
from mev_inspect.inspect_block import inspect_block
from mev_inspect.provider import get_base_provider
from mev_inspect.block import create_from_block_number


RPC_URL_ENV = "RPC_URL"

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("block_number", type=int)
@click.option("--rpc", default=lambda: os.environ.get(RPC_URL_ENV, ""))
@click.option("--cache/--no-cache", default=True)
def inspect_block_command(block_number: int, rpc: str, cache: bool):
    inspect_db_session = get_inspect_session()
    trace_db_session = get_trace_session()

    base_provider = get_base_provider(rpc)
    w3 = Web3(base_provider)
    trace_classifier = TraceClassifier()

    if not cache:
        logger.info("Skipping cache")

    inspect_block(
        inspect_db_session,
        base_provider,
        w3,
        trace_classifier,
        block_number,
        trace_db_session=trace_db_session,
    )


@cli.command()
@click.argument("block_number", type=int)
@click.option("--rpc", default=lambda: os.environ.get(RPC_URL_ENV, ""))
def fetch_block_command(block_number: int, rpc: str):
    base_provider = get_base_provider(rpc)
    w3 = Web3(base_provider)
    trace_db_session = get_trace_session()

    block = create_from_block_number(
        base_provider,
        w3,
        block_number,
        trace_db_session=trace_db_session,
    )

    print(block)


@cli.command()
@click.argument("after_block", type=int)
@click.argument("before_block", type=int)
@click.option("--rpc", default=lambda: os.environ.get(RPC_URL_ENV, ""))
@click.option("--cache/--no-cache", default=True)
def inspect_many_blocks_command(
    after_block: int, before_block: int, rpc: str, cache: bool
):

    inspect_db_session = get_inspect_session()
    trace_db_session = get_trace_session()

    base_provider = get_base_provider(rpc)
    w3 = Web3(base_provider)
    trace_classifier = TraceClassifier()

    if not cache:
        logger.info("Skipping cache")

    for i, block_number in enumerate(range(after_block, before_block)):
        block_message = (
            f"Running for {block_number} ({i+1}/{before_block - after_block})"
        )
        dashes = "-" * len(block_message)
        logger.info(dashes)
        logger.info(block_message)
        logger.info(dashes)

        inspect_block(
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
