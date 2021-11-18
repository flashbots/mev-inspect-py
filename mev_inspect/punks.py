from typing import List
from mev_inspect.schemas import punk_accept_bid

from mev_inspect.schemas.traces import (
    ClassifiedTrace,
    Classification,
    DecodedCallTrace,
)
from mev_inspect.schemas.punk_bid import PunkBid
from mev_inspect.schemas.punk_accept_bid import PunkBidAcceptance
from mev_inspect.traces import get_traces_by_transaction_hash


def get_punk_bid_acceptances(traces: List[ClassifiedTrace]) -> List[PunkBidAcceptance]:
    punk_bid_acceptances = []

    for _, transaction_traces in get_traces_by_transaction_hash(traces).items():
        punk_bid_acceptances += _get_punk_bid_acceptances_for_transaction(
            list(transaction_traces)
        )

    return punk_bid_acceptances


def _get_punk_bid_acceptances_for_transaction(
    traces: List[ClassifiedTrace],
) -> List[PunkBidAcceptance]:
    ordered_traces = list(sorted(traces, key=lambda t: t.trace_address))

    punk_bid_acceptances = []

    for trace in ordered_traces:
        if not isinstance(trace, DecodedCallTrace):
            continue

        elif trace.classification == Classification.punk_accept_bid:
            punk_accept_bid = PunkBidAcceptance(
                block_number=trace.block_number,
                transaction_hash=trace.transaction_hash,
                trace_address=trace.trace_address,
                from_address=trace.from_address,
                punk_index=trace.inputs["punk_index"],
                min_price=trace.inputs["min_price"],
            )

            punk_bid_acceptances.append(punk_accept_bid)

    return punk_bid_acceptances


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
