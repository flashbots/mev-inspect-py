from typing import Optional, List, Sequence

from mev_inspect.schemas.swaps import Swap
from mev_inspect.schemas.transfers import Transfer, ETH_TOKEN_ADDRESS

from mev_inspect.schemas.traces import DecodedCallTrace, ClassifiedTrace


def create_swap_from_pool_transfers(
    trace: DecodedCallTrace,
    recipient_address: str,
    prior_transfers: List[Transfer],
    child_transfers: List[Transfer],
) -> Optional[Swap]:
    pool_address = trace.to_address

    transfers_to_pool = []

    if trace.value is not None and trace.value > 0:
        transfers_to_pool = [_build_eth_transfer(trace)]

    if len(transfers_to_pool) == 0:
        transfers_to_pool = _filter_transfers(prior_transfers, to_address=pool_address)

    if len(transfers_to_pool) == 0:
        transfers_to_pool = _filter_transfers(child_transfers, to_address=pool_address)

    if len(transfers_to_pool) == 0:
        return None

    transfers_from_pool_to_recipient = _filter_transfers(
        child_transfers, to_address=recipient_address, from_address=pool_address
    )

    if len(transfers_from_pool_to_recipient) != 1:
        return None

    transfer_in = transfers_to_pool[-1]
    transfer_out = transfers_from_pool_to_recipient[0]

    return Swap(
        abi_name=trace.abi_name,
        transaction_hash=trace.transaction_hash,
        block_number=trace.block_number,
        trace_address=trace.trace_address,
        contract_address=pool_address,
        protocol=trace.protocol,
        from_address=transfer_in.from_address,
        to_address=transfer_out.to_address,
        token_in_address=transfer_in.token_address,
        token_in_amount=transfer_in.amount,
        token_out_address=transfer_out.token_address,
        token_out_amount=transfer_out.amount,
        error=trace.error,
    )


def create_swap_from_recipient_transfers(
    trace: DecodedCallTrace,
    pool_address: str,
    recipient_address: str,
    prior_transfers: List[Transfer],
    child_transfers: List[Transfer],
) -> Optional[Swap]:
    transfers_from_recipient = _filter_transfers(
        [*prior_transfers, *child_transfers], from_address=recipient_address
    )
    transfers_to_recipient = _filter_transfers(
        child_transfers, to_address=recipient_address
    )

    if len(transfers_from_recipient) != 1 or len(transfers_to_recipient) != 1:
        return None

    transfer_in = transfers_from_recipient[0]
    transfer_out = transfers_to_recipient[0]

    return Swap(
        abi_name=trace.abi_name,
        transaction_hash=trace.transaction_hash,
        block_number=trace.block_number,
        trace_address=trace.trace_address,
        contract_address=pool_address,
        protocol=trace.protocol,
        from_address=transfer_in.from_address,
        to_address=transfer_out.to_address,
        token_in_address=transfer_in.token_address,
        token_in_amount=transfer_in.amount,
        token_out_address=transfer_out.token_address,
        token_out_amount=transfer_out.amount,
        error=trace.error,
    )


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


def _filter_transfers(
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
