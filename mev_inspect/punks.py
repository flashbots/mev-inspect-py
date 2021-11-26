from typing import List, Optional
from mev_inspect.schemas.traces import (
    ClassifiedTrace,
    Classification,
    DecodedCallTrace,
)
from mev_inspect.schemas.punk_bid import PunkBid
from mev_inspect.schemas.punk_accept_bid import PunkBidAcceptance
from mev_inspect.schemas.punk_snipe import PunkSnipe
from mev_inspect.traces import get_traces_by_transaction_hash


def _get_highest_punk_bid_per_index(
    punk_bids: List[PunkBid], punk_index: int
) -> Optional[PunkBid]:
    highest_punk_bid = None

    for punk_bid in punk_bids:
        if punk_bid.punk_index == punk_index:
            if highest_punk_bid is None:
                highest_punk_bid = punk_bid

            elif punk_bid.price > highest_punk_bid.price:
                highest_punk_bid = punk_bid

    return highest_punk_bid


def get_punk_snipes(
    punk_bids: List[PunkBid], punk_bid_acceptances: List[PunkBidAcceptance]
) -> List[PunkSnipe]:
    punk_snipe_list = []

    for punk_bid_acceptance in punk_bid_acceptances:
        highest_punk_bid = _get_highest_punk_bid_per_index(
            punk_bids, punk_bid_acceptance.punk_index
        )

        if highest_punk_bid is None:
            continue

        if highest_punk_bid.price > punk_bid_acceptance.min_price:
            punk_snipe = PunkSnipe(
                block_number=highest_punk_bid.block_number,
                transaction_hash=highest_punk_bid.transaction_hash,
                trace_address=highest_punk_bid.trace_address,
                from_address=highest_punk_bid.from_address,
                punk_index=highest_punk_bid.punk_index,
                min_acceptance_price=punk_bid_acceptance.min_price,
                acceptance_price=highest_punk_bid.price,
            )

            punk_snipe_list.append(punk_snipe)

    return punk_snipe_list


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
                punk_index=trace.inputs["punkIndex"],
                min_price=trace.inputs["minPrice"],
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
                punk_index=trace.inputs["punkIndex"],
                price=trace.value,
            )

            punk_bids.append(punk_bid)

    return punk_bids
