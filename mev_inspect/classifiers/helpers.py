from typing import Optional, List, Sequence, Tuple

from mev_inspect.schemas.swaps import Swap
from mev_inspect.schemas.transfers import Transfer, ETH_TOKEN_ADDRESS

from mev_inspect.schemas.traces import DecodedCallTrace, ClassifiedTrace


RFQ_SIGNATURES = [
    "fillRfqOrder((address,address,uint128,uint128,address,address,address,bytes32,uint64,uint256),(uint8,uint8,bytes32,bytes32),uint128)",
    "_fillRfqOrder((address,address,uint128,uint128,address,address,address,bytes32,uint64,uint256),(uint8,uint8,bytes32,bytes32),uint128,address,bool,address)",
]
LIMIT_SIGNATURES = [
    "fillOrKillLimitOrder((address,address,uint128,uint128,uint128,address,address,address,address,bytes32,uint64,uint256),(uint8,uint8,bytes32,bytes32),uint128)",
    "fillLimitOrder((address,address,uint128,uint128,uint128,address,address,address,address,bytes32,uint64,uint256),(uint8,uint8,bytes32,bytes32),uint128)",
    "_fillLimitOrder((address,address,uint128,uint128,uint128,address,address,address,address,bytes32,uint64,uint256),(uint8,uint8,bytes32,bytes32),uint128,address,address)",
]


def create_swap_from_transfers(
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


def is_valid_0x_swap(
    trace: DecodedCallTrace,
    child_transfers: List[Transfer],
) -> bool:

    # 1. There should be 2 child transfers, one for each settled leg of the order
    if len(child_transfers) != 2:
        raise ValueError(
            f"A settled order should consist of 2 child transfers, not {len(child_transfers)}."
        )

    # 2. The function signature must be in the lists of supported signatures
    if trace.function_signature not in (LIMIT_SIGNATURES + RFQ_SIGNATURES):
        raise RuntimeError(
            f"0x orderbook function {trace.function_signature} is not supported"
        )

    return True


def _get_taker_token_in_amount(
    taker_address: str, token_in_address: str, child_transfers: List[Transfer]
) -> int:

    ANY_TAKER = "0x0000000000000000000000000000000000000000"

    if taker_address == ANY_TAKER:
        for transfer in child_transfers:
            if transfer.token_address == token_in_address:
                return transfer.amount
    else:
        for transfer in child_transfers:
            if transfer.to_address == taker_address:
                return transfer.amount
    return 0


def get_0x_token_in_data(
    trace: DecodedCallTrace, child_transfers: List[Transfer]
) -> Tuple[str, int]:

    order: List = trace.inputs["order"]
    token_in_address = order[0]

    if trace.function_signature in RFQ_SIGNATURES:
        taker_address = order[5]

    elif trace.function_signature in LIMIT_SIGNATURES:
        taker_address = order[6]

    token_in_amount = _get_taker_token_in_amount(
        taker_address, token_in_address, child_transfers
    )

    return token_in_address, token_in_amount


def get_0x_token_out_data(trace: DecodedCallTrace) -> Tuple[str, int]:

    order: List = trace.inputs["order"]
    token_out_address = order[1]
    token_out_amount = trace.inputs["takerTokenFillAmount"]

    return token_out_address, token_out_amount
