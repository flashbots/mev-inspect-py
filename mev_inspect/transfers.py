from typing import List, Optional

from mev_inspect.schemas.classified_traces import Classification, ClassifiedTrace
from mev_inspect.schemas.transfers import Transfer
from mev_inspect.traces import is_child_trace_address, get_child_traces


def get_child_transfers(
    parent_trace_address: List[int],
    traces: List[ClassifiedTrace],
) -> List[Transfer]:
    child_transfers = []

    for child_trace in get_child_traces(parent_trace_address, traces):
        if child_trace.classification == Classification.transfer:
            child_transfers.append(Transfer.from_trace(child_trace))

    return child_transfers


def filter_transfers(
    transfers: List[Transfer],
    to_address: Optional[str] = None,
    from_address: Optional[str] = None,
) -> List[Transfer]:
    filtered_transfers = []

    for transfer in transfers:
        if to_address is not None and transfer.to_address != to_address:
            continue

        if from_address is not None and transfer.from_address != from_address:
            continue

        filtered_transfers.append(transfer)

    return filtered_transfers


def remove_inner_transfers(transfers: List[Transfer]) -> List[Transfer]:
    updated_transfers = []
    transfer_trace_addresses: List[List[int]] = []

    sorted_transfers = sorted(transfers, key=lambda t: t.trace_address)

    for transfer in sorted_transfers:
        if not any(
            is_child_trace_address(transfer.trace_address, parent_address)
            for parent_address in transfer_trace_addresses
        ):
            updated_transfers.append(transfer)

        transfer_trace_addresses.append(transfer.trace_address)

    return updated_transfers
