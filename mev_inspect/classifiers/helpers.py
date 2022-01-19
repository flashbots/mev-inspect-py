from typing import List, Optional, Sequence

from mev_inspect.schemas.nft_trades import NftTrade
from mev_inspect.schemas.prices import ETH_TOKEN_ADDRESS
from mev_inspect.schemas.swaps import Swap
from mev_inspect.schemas.traces import ClassifiedTrace, DecodedCallTrace
from mev_inspect.schemas.transfers import Transfer


def create_nft_trade_from_transfers(
    trace: DecodedCallTrace,
    child_transfers: List[Transfer],
    collection_address: str,
    seller_address: str,
    buyer_address: str,
    exchange_wallet_address: str,
) -> Optional[NftTrade]:
    transfers_to_buyer = _filter_transfers(child_transfers, to_address=buyer_address)
    transfers_to_seller = _filter_transfers(child_transfers, to_address=seller_address)

    if len(transfers_to_buyer) != 1 or len(transfers_to_seller) != 1:
        return None

    if transfers_to_buyer[0].token_address != collection_address:
        return None

    payment_token_address = transfers_to_seller[0].token_address
    payment_amount = transfers_to_seller[0].amount
    token_id = transfers_to_buyer[0].amount

    transfers_from_seller_to_exchange = _filter_transfers(
        child_transfers,
        from_address=seller_address,
        to_address=exchange_wallet_address,
    )
    transfers_from_buyer_to_exchange = _filter_transfers(
        child_transfers,
        from_address=buyer_address,
        to_address=exchange_wallet_address,
    )
    for fee in [
        *transfers_from_seller_to_exchange,
        *transfers_from_buyer_to_exchange,
    ]:
        # Assumes that exchange fees are paid with the same token as the sale
        payment_amount -= fee.amount

    return NftTrade(
        abi_name=trace.abi_name,
        transaction_hash=trace.transaction_hash,
        transaction_position=trace.transaction_position,
        block_number=trace.block_number,
        trace_address=trace.trace_address,
        protocol=trace.protocol,
        error=trace.error,
        seller_address=seller_address,
        buyer_address=buyer_address,
        payment_token_address=payment_token_address,
        payment_amount=payment_amount,
        collection_address=collection_address,
        token_id=token_id,
    )


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
        transaction_position=trace.transaction_position,
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
        transaction_position=trace.transaction_position,
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


def get_received_transfer(
    liquidator: str, child_transfers: List[Transfer]
) -> Optional[Transfer]:
    """Get transfer from AAVE to liquidator"""

    for transfer in child_transfers:
        if transfer.to_address == liquidator:
            return transfer

    return None


def get_debt_transfer(
    liquidator: str, child_transfers: List[Transfer]
) -> Optional[Transfer]:
    """Get transfer from liquidator to AAVE"""

    for transfer in child_transfers:
        if transfer.from_address == liquidator:
            return transfer

    return None
