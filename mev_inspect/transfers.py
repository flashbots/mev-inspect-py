from typing import Dict, List, Optional, Sequence

from mev_inspect.classifiers.specs import get_classifier
from mev_inspect.schemas.classifiers import TransferClassifier
from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    DecodedCallTrace,
)
from mev_inspect.schemas.transfers import ETH_TOKEN_ADDRESS, Transfer
from mev_inspect.traces import is_child_trace_address, get_child_traces


def get_transfers(traces: List[ClassifiedTrace]) -> List[Transfer]:
    transfers = []

    for trace in traces:
        transfer = get_transfer(trace)
        if transfer is not None:
            transfers.append(transfer)

    return transfers


def get_eth_transfers(traces: List[ClassifiedTrace]) -> List[Transfer]:
    transfers = get_transfers(traces)

    return [
        transfer
        for transfer in transfers
        if transfer.token_address == ETH_TOKEN_ADDRESS
    ]


def get_transfer(trace: ClassifiedTrace) -> Optional[Transfer]:
    if trace.value is not None and trace.value > 0:
        return _build_eth_transfer(trace)

    if isinstance(trace, DecodedCallTrace):
        return _build_erc20_transfer(trace)

    return None


def _build_eth_transfer(trace: ClassifiedTrace) -> Transfer:
    return Transfer(
        block_number=trace.block_number,
        transaction_hash=trace.transaction_hash,
        trace_address=trace.trace_address,
        amount=trace.value,
        to_address=trace.to_address,
        from_address=trace.from_address,
        token_address=ETH_TOKEN_ADDRESS,
    )


def _build_erc20_transfer(trace: DecodedCallTrace) -> Optional[Transfer]:
    classifier = get_classifier(trace)
    if classifier is not None and issubclass(classifier, TransferClassifier):
        return classifier.get_transfer(trace)

    return None


def get_child_transfers(
    transaction_hash: str,
    parent_trace_address: List[int],
    traces: List[ClassifiedTrace],
) -> List[Transfer]:
    child_transfers = []

    for child_trace in get_child_traces(transaction_hash, parent_trace_address, traces):
        transfer = get_transfer(child_trace)
        if transfer is not None:
            child_transfers.append(transfer)

    return child_transfers


def filter_transfers(
    transfers: Sequence[Transfer],
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


def remove_child_transfers_of_transfers(
    transfers: List[Transfer],
) -> List[Transfer]:
    updated_transfers = []
    transfer_addresses_by_transaction: Dict[str, List[List[int]]] = {}

    sorted_transfers = sorted(transfers, key=lambda t: t.trace_address)

    for transfer in sorted_transfers:
        existing_addresses = transfer_addresses_by_transaction.get(
            transfer.transaction_hash, []
        )

        if not any(
            is_child_trace_address(transfer.trace_address, parent_address)
            for parent_address in existing_addresses
        ):
            updated_transfers.append(transfer)

        transfer_addresses_by_transaction[
            transfer.transaction_hash
        ] = existing_addresses + [transfer.trace_address]

    return updated_transfers
