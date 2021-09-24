from itertools import groupby
from typing import Dict, List

from mev_inspect.schemas.classified_traces import ClassifiedTrace


def is_child_trace_address(
    child_trace_address: List[int],
    parent_trace_address: List[int],
) -> bool:
    parent_trace_length = len(parent_trace_address)

    return (
        len(child_trace_address) > parent_trace_length
        and child_trace_address[:parent_trace_length] == parent_trace_address
    )


def get_child_traces(
    transaction_hash: str,
    parent_trace_address: List[int],
    traces: List[ClassifiedTrace],
) -> List[ClassifiedTrace]:
    ordered_traces = sorted(traces, key=lambda t: t.trace_address)
    child_traces = []

    for trace in ordered_traces:
        if trace.transaction_hash == transaction_hash and is_child_trace_address(
            trace.trace_address,
            parent_trace_address,
        ):
            child_traces.append(trace)

    return child_traces


def is_child_of_any_address(
    trace: ClassifiedTrace, parent_trace_addresses: List[List[int]]
) -> bool:

    return any(
        [
            is_child_trace_address(trace.trace_address, parent)
            for parent in parent_trace_addresses
        ]
    )


def get_traces_by_transaction_hash(
    traces: List[ClassifiedTrace],
) -> Dict[str, List[ClassifiedTrace]]:
    get_transaction_hash = lambda trace: trace.transaction_hash
    return {
        transaction_hash: list(traces)
        for transaction_hash, traces in groupby(
            sorted(traces, key=get_transaction_hash),
            key=get_transaction_hash,
        )
    }
