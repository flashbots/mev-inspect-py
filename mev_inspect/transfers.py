from typing import Dict, List, Optional, Sequence

from mev_inspect.classifiers.specs import get_classifier
from mev_inspect.schemas.classifiers import TransferClassifier
from mev_inspect.schemas.prices import ETH_TOKEN_ADDRESS
from mev_inspect.schemas.traces import Classification, ClassifiedTrace, DecodedCallTrace
from mev_inspect.schemas.transfers import Transfer
from mev_inspect.traces import get_child_traces, is_child_trace_address


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
    if _is_simple_eth_transfer(trace):
        return build_eth_transfer(trace)

    if isinstance(trace, DecodedCallTrace):
        return _build_erc20_transfer(trace)

    return None


def _is_simple_eth_transfer(trace: ClassifiedTrace) -> bool:
    return (
        trace.value is not None
        and trace.value > 0
        and "input" in trace.action
        and trace.action["input"] == "0x"
    )


def build_eth_transfer(trace: ClassifiedTrace) -> Transfer:
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


def get_net_transfers(
    classified_traces: List[ClassifiedTrace],
) -> List[Transfer]:
    """
    Returns the net transfers per transaction from a list of Classified Traces.
    If A transfers 200WETH to B ,and later in the transaction, B transfers 50WETH to A,
    the following transfer would be returned  (from_address=A, to_address=B, amount=150)

    If B transferred 300WETH to A, the following would be returned
    (from_address=contract, to_address=bot, amount=100)

    If B transferred 200WETH to A, no transfer would be returned
    @param classified_traces:
    @return: List of Transfer objects representing the net movement of tokens
    """
    found_transfers: List[list] = []
    return_transfers: List[Transfer] = []
    for trace in classified_traces:
        if not isinstance(trace, DecodedCallTrace):
            continue

        if trace.classification == Classification.transfer:
            if trace.from_address in [
                t.token_address for t in return_transfers
            ]:  # Proxy Case
                continue

            if trace.function_signature == "transfer(address,uint256)":
                net_search_info = {
                    "to_address": trace.inputs["recipient"],
                    "token_address": trace.to_address,
                    "from_address": trace.from_address,
                }

            elif trace.function_signature == "transferFrom(address,address,uint256)":
                net_search_info = {
                    "to_address": trace.inputs["recipient"],
                    "token_address": trace.to_address,
                    "from_address": trace.inputs["sender"],
                }

            else:
                continue

            if sorted(list(net_search_info.values())) in found_transfers:
                for index, transfer in enumerate(return_transfers):
                    if (
                        transfer.token_address != net_search_info["token_address"]
                        or transfer.transaction_hash != trace.transaction_hash
                    ):
                        continue

                    if (
                        transfer.from_address == net_search_info["from_address"]
                        and transfer.to_address == net_search_info["to_address"]
                    ):
                        return_transfers[index].amount += trace.inputs["amount"]
                        return_transfers[index].trace_address = [-1]
                    if (
                        transfer.from_address == net_search_info["to_address"]
                        and transfer.to_address == net_search_info["from_address"]
                    ):
                        return_transfers[index].amount -= trace.inputs["amount"]
                        return_transfers[index].trace_address = [-1]

            else:
                return_transfers.append(
                    Transfer(
                        block_number=trace.block_number,
                        transaction_hash=trace.transaction_hash,
                        trace_address=trace.trace_address,
                        from_address=net_search_info["from_address"],
                        to_address=net_search_info["to_address"],
                        amount=trace.inputs["amount"],
                        token_address=net_search_info["token_address"],
                    )
                )
                found_transfers.append(sorted(list(net_search_info.values())))

    process_index = -1
    while True:
        process_index += 1
        try:
            transfer = return_transfers[process_index]
        except IndexError:
            break
        if transfer.amount < 0:
            return_transfers[process_index].from_address = transfer.to_address
            return_transfers[process_index].to_address = transfer.from_address
            return_transfers[process_index].amount = transfer.amount * -1
        if transfer.amount == 0:
            return_transfers.pop(process_index)
            process_index -= 1

    return return_transfers
