import argparse
import json

from web3 import Web3

from mev_inspect import block
from mev_inspect.crud.classified_traces import write_classified_traces
from mev_inspect.db import get_session
from mev_inspect.classifier_specs import CLASSIFIER_SPECS
from mev_inspect.trace_classifier import TraceClassifier


def inspect_block(base_provider, block_number):
    block_data = block.create_from_block_number(block_number, base_provider)
    print(f"Total traces: {len(block_data.traces)}")

    total_transactions = len(
        set(
            t.transaction_hash
            for t in block_data.traces
            if t.transaction_hash is not None
        )
    )
    print(f"Total transactions: {total_transactions}")

    trace_clasifier = TraceClassifier(CLASSIFIER_SPECS)
    classified_traces = trace_clasifier.classify(block_data.traces)
    print(f"Returned {len(classified_traces)} classified traces")

    db_session = get_session()
    write_classified_traces(db_session, classified_traces)
    db_session.close()

    stats = get_stats(classified_traces)
    print(json.dumps(stats, indent=4))


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
    parser = argparse.ArgumentParser(description="Inspect some blocks.")

    parser.add_argument(
        "-block_number",
        metavar="b",
        type=int,
        nargs="+",
        help="the block number you are targetting, eventually this will need to be changed",
    )

    parser.add_argument(
        "-rpc", metavar="r", help="rpc endpoint, this needs to have parity style traces"
    )

    args = parser.parse_args()

    w3_base_provider = Web3.HTTPProvider(args.rpc)
    inspect_block(w3_base_provider, args.block_number[0])
