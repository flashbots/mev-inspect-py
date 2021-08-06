import json

import click
from web3 import Web3

from mev_inspect import block
from mev_inspect.crud.arbitrages import (
    delete_arbitrages_for_block,
    write_arbitrages,
)
from mev_inspect.crud.classified_traces import (
    delete_classified_traces_for_block,
    write_classified_traces,
)
from mev_inspect.crud.swaps import delete_swaps_for_block, write_swaps
from mev_inspect.db import get_session
from mev_inspect.classifier_specs import CLASSIFIER_SPECS
from mev_inspect.trace_classifier import TraceClassifier
from mev_inspect.arbitrages import get_arbitrages
from mev_inspect.swaps import get_swaps


@click.group()
def cli():
    pass


@cli.command()
@click.argument("block_number", type=int)
@click.argument("rpc")
def inspect_block(block_number: int, rpc: str):
    base_provider = Web3.HTTPProvider(rpc)
    _inspect_block(base_provider, block_number)


@cli.command()
@click.argument("after_block", type=int)
@click.argument("before_block", type=int)
@click.argument("rpc")
def inspect_many_blocks(after_block: int, before_block: int, rpc: str):
    base_provider = Web3.HTTPProvider(rpc)
    for block_number in range(after_block + 1, before_block):
        _inspect_block(
            base_provider,
            block_number,
            should_print_stats=False,
            should_write_classified_traces=False,
        )


def _inspect_block(
    base_provider,
    block_number: int,
    should_print_stats: bool = True,
    should_write_classified_traces: bool = True,
    should_write_swaps: bool = True,
    should_write_arbitrages: bool = True,
):

    block_message = f"Running for {block_number}"
    dashes = "-" * len(block_message)
    click.echo(dashes)
    click.echo(block_message)
    click.echo(dashes)

    block_data = block.create_from_block_number(block_number, base_provider)
    click.echo(f"Total traces: {len(block_data.traces)}")

    total_transactions = len(
        set(
            t.transaction_hash
            for t in block_data.traces
            if t.transaction_hash is not None
        )
    )
    click.echo(f"Total transactions: {total_transactions}")

    trace_clasifier = TraceClassifier(CLASSIFIER_SPECS)
    classified_traces = trace_clasifier.classify(block_data.traces)
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

    if should_print_stats:
        stats = get_stats(classified_traces)
        click.echo(json.dumps(stats, indent=4))


def get_stats(classified_traces) -> dict:
    stats: dict = {}

    for trace in classified_traces:
        abi_name = trace.abi_name
        classification = trace.classification.value
        signature = trace.function_signature

        abi_name_stats = stats.get(abi_name, {})
        class_stats = abi_name_stats.get(classification, {})
        signature_count = class_stats.get(signature, 0)
        class_stats[signature] = signature_count + 1
        abi_name_stats[classification] = class_stats
        stats[abi_name] = abi_name_stats

    return stats


if __name__ == "__main__":
    cli()
