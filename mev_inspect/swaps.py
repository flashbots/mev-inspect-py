from typing import List, Optional

from mev_inspect.classifiers.specs import get_classifier
from mev_inspect.schemas.classifiers import SwapClassifier
from mev_inspect.schemas.swaps import Swap
from mev_inspect.schemas.traces import Classification, ClassifiedTrace, DecodedCallTrace
from mev_inspect.schemas.transfers import Transfer
from mev_inspect.traces import get_traces_by_transaction_hash
from mev_inspect.transfers import (
    get_child_transfers,
    get_transfer,
    remove_child_transfers_of_transfers,
)


def get_swaps(traces: List[ClassifiedTrace]) -> List[Swap]:
    swaps = []

    for _, transaction_traces in get_traces_by_transaction_hash(traces).items():
        swaps += _get_swaps_for_transaction(list(transaction_traces))

    return swaps


def _get_swaps_for_transaction(traces: List[ClassifiedTrace]) -> List[Swap]:
    ordered_traces = list(sorted(traces, key=lambda t: t.trace_address))

    swaps: List[Swap] = []
    prior_transfers: List[Transfer] = []

    for trace in ordered_traces:
        if not isinstance(trace, DecodedCallTrace):
            continue

        elif trace.classification == Classification.transfer:
            transfer = get_transfer(trace)
            if transfer is not None:
                prior_transfers.append(transfer)

        elif trace.classification == Classification.swap:
            child_transfers = get_child_transfers(
                trace.transaction_hash,
                trace.trace_address,
                traces,
            )

            swap = _parse_swap(
                trace,
                remove_child_transfers_of_transfers(prior_transfers),
                remove_child_transfers_of_transfers(child_transfers),
            )

            if swap is not None:
                swaps.append(swap)

    return swaps


def _parse_swap(
    trace: DecodedCallTrace,
    prior_transfers: List[Transfer],
    child_transfers: List[Transfer],
) -> Optional[Swap]:

    classifier = get_classifier(trace)
    if classifier is not None and issubclass(classifier, SwapClassifier):
        return classifier.parse_swap(trace, prior_transfers, child_transfers)
    return None
