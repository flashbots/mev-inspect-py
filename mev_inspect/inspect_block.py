import json

import click
from web3 import Web3

from mev_inspect.arbitrages import get_arbitrages
from mev_inspect.block import create_from_block_number
from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.crud.arbitrages import (
    delete_arbitrages_for_block,
    write_arbitrages,
)
from mev_inspect.crud.classified_traces import (
    delete_classified_traces_for_block,
    write_classified_traces,
)
from mev_inspect.crud.miner_payments import (
    delete_miner_payments_for_block,
    write_miner_payments,
)
from mev_inspect.crud.swaps import delete_swaps_for_block, write_swaps
from mev_inspect.db import get_session
from mev_inspect.miner_payments import get_miner_payments
from mev_inspect.swaps import get_swaps
from mev_inspect.retry import http_retry_with_backoff_request_middleware
from mev_inspect.aave_liquidations import find_liquidations_from_traces


@click.group()
def cli():
    pass


@cli.command()
@click.argument("block_number", type=int)
@click.argument("rpc")
@click.option("--cache/--no-cache", default=True)
def inspect_block(block_number: int, rpc: str, cache: bool):
    base_provider = _get_base_provider(rpc)
    w3 = Web3(base_provider)

    if not cache:
        click.echo("Skipping cache")

    _inspect_block(base_provider, w3, block_number, should_cache=cache)


@cli.command()
@click.argument("after_block", type=int)
@click.argument("before_block", type=int)
@click.argument("rpc")
@click.option("--cache/--no-cache", default=True)
def inspect_many_blocks(after_block: int, before_block: int, rpc: str, cache: bool):
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

        _inspect_block(
            base_provider,
            w3,
            block_number,
            should_print_stats=False,
            should_write_classified_traces=False,
            should_cache=cache,
        )


def _inspect_block(
    base_provider,
    w3: Web3,
    block_number: int,
    should_cache: bool,
    should_print_stats: bool = True,
    should_print_miner_payments: bool = True,
    should_write_classified_traces: bool = True,
    should_write_swaps: bool = True,
    should_write_arbitrages: bool = True,
    should_write_miner_payments: bool = True,
):
    block = create_from_block_number(base_provider, w3, block_number, should_cache)

    click.echo(f"Total traces: {len(block.traces)}")

    total_transactions = len(
        set(t.transaction_hash for t in block.traces if t.transaction_hash is not None)
    )
    click.echo(f"Total transactions: {total_transactions}")

    trace_clasifier = TraceClassifier()
    classified_traces = trace_clasifier.classify(block.traces)
    click.echo(f"Returned {len(classified_traces)} classified traces")

    db_session = get_session()

    if should_write_classified_traces:
        delete_classified_traces_for_block(db_session, block_number)
        write_classified_traces(db_session, classified_traces)

    swaps = get_swaps(classified_traces)
    click.echo(f"Found {len(swaps)} swaps")

    if should_write_swaps:
        delete_swaps_for_block(db_session, block_number)
        write_swaps(db_session, swaps)

    arbitrages = get_arbitrages(swaps)
    click.echo(f"Found {len(arbitrages)} arbitrages")

    if should_write_arbitrages:
        delete_arbitrages_for_block(db_session, block_number)
        write_arbitrages(db_session, arbitrages)

    liquidations = find_liquidations_from_traces(classified_traces)
    click.echo(f"Found {len(liquidations)} liquidations")
    print(liquidations)

    if should_print_stats:
        stats = get_stats(classified_traces)
        click.echo(json.dumps(stats, indent=4))

    miner_payments = get_miner_payments(
        block.miner, block.base_fee_per_gas, classified_traces, block.receipts
    )

    if should_print_miner_payments:
        click.echo(json.dumps([p.dict() for p in miner_payments], indent=4))

    if should_write_miner_payments:
        delete_miner_payments_for_block(db_session, block_number)
        write_miner_payments(db_session, miner_payments)


def get_stats(classified_traces) -> dict:
    stats: dict = {}

    for trace in classified_traces:
        protocol = str(trace.protocol)
        abi_name = trace.abi_name
        classification = trace.classification.value
        signature = trace.function_signature

        protocol_stats = stats.get(protocol, {})
        abi_name_stats = protocol_stats.get(abi_name, {})
        class_stats = abi_name_stats.get(classification, {})
        signature_count = class_stats.get(signature, 0)
        class_stats[signature] = signature_count + 1
        abi_name_stats[classification] = class_stats
        protocol_stats[abi_name] = abi_name_stats
        stats[protocol] = protocol_stats

    return stats


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
