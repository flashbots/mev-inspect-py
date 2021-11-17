from typing import List

from mev_inspect.schemas.traces import (
    ClassifiedTrace,
    Classification,
    DecodedCallTrace,
)
from mev_inspect.schemas.punk_bid import PunkBid
from mev_inspect.schemas.punk_accept_bid import PunkAcceptBid
from mev_inspect.traces import get_traces_by_transaction_hash


def get_punk_accept_bids(traces: List[ClassifiedTrace]) -> List[PunkAcceptBid]:
    punk_accept_bids = []

    for _, transaction_traces in get_traces_by_transaction_hash(traces).items():
        punk_accept_bids += _get_punk_accept_bids_for_transaction(
            list(transaction_traces)
        )

    return punk_accept_bids


def _get_punk_accept_bids_for_transaction(
    traces: List[ClassifiedTrace],
) -> List[PunkAcceptBid]:
    ordered_traces = list(sorted(traces, key=lambda t: t.trace_address))

    punk_accept_bids = []

    for trace in ordered_traces:
        if not isinstance(trace, DecodedCallTrace):
            continue

        elif trace.classification == Classification.punk_accept_bid:
            punk_accept_bid = PunkAcceptBid(
                block_number=trace.block_number,
                transaction_hash=trace.transaction_hash,
                trace_address=trace.trace_address,
                from_address=trace.from_address,
                punk_index=trace.inputs["punk_index"],
                min_price=trace.inputs["min_price"],
            )

            punk_accept_bids.append(punk_accept_bid)

    return punk_accept_bids


def get_punk_bids(traces: List[ClassifiedTrace]) -> List[PunkBid]:
    punk_bids = []

    for _, transaction_traces in get_traces_by_transaction_hash(traces).items():
        punk_bids += _get_punk_bids_for_transaction(list(transaction_traces))

    return punk_bids


def _get_punk_bids_for_transaction(traces: List[ClassifiedTrace]) -> List[PunkBid]:
    ordered_traces = list(sorted(traces, key=lambda t: t.trace_address))

    punk_bids = []

    for trace in ordered_traces:
        if not isinstance(trace, DecodedCallTrace):
            continue

        elif trace.classification == Classification.punk_bid:
            punk_bid = PunkBid(
                transaction_hash=trace.transaction_hash,
                block_number=trace.block_number,
                trace_address=trace.trace_address,
                from_address=trace.from_address,
                punk_index=trace.inputs["punk_index"],
                value=trace.value,
            )

            punk_bids.append(punk_bid)

    return punk_bids
