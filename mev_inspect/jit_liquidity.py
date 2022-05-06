from typing import List, Tuple

from pydantic import BaseModel

from mev_inspect.schemas.jit_liquidity import JITLiquidity
from mev_inspect.schemas.swaps import Swap
from mev_inspect.schemas.traces import (
    Classification,
    ClassifiedTrace,
    DecodedCallTrace,
    Protocol,
)
from mev_inspect.schemas.transfers import Transfer
from mev_inspect.traces import is_child_trace_address
from mev_inspect.transfers import get_net_transfers

LIQUIDITY_MINT_ROUTERS = [
    "0xC36442b4a4522E871399CD717aBDD847Ab11FE88".lower(),  # Uniswap V3 NFT Position Manager
]

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


class JITTransferInfo(BaseModel):
    token0_address: str
    token1_address: str
    mint_token0: int
    mint_token1: int
    burn_token0: int
    burn_token1: int
    error: bool


def get_jit_liquidity(
    classified_traces: List[ClassifiedTrace], swaps: List[Swap]
) -> List[JITLiquidity]:
    jit_liquidity_instances: List[JITLiquidity] = []

    for index, trace in enumerate(classified_traces):

        if not isinstance(trace, DecodedCallTrace):
            continue

        if (
            trace.classification == Classification.liquidity_mint
            and trace.protocol == Protocol.uniswap_v3
        ):
            for search_trace in classified_traces[index:]:
                if (
                    search_trace.classification == Classification.liquidity_burn
                    and search_trace.to_address == trace.to_address
                ):

                    bot_address = _get_bot_address(trace, classified_traces)
                    transfer_info: JITTransferInfo = _get_transfer_info(
                        classified_traces,
                        trace,
                        search_trace,
                    )
                    jit_swaps, token0_volume, token1_volume = _get_swap_info(
                        swaps, trace, search_trace, transfer_info.token0_address
                    )

                    # -- Error Checking Section --
                    if transfer_info.error or len(jit_swaps) == 0:
                        continue

                    jit_liquidity_instances.append(
                        JITLiquidity(
                            block_number=trace.block_number,
                            bot_address=bot_address,
                            pool_address=trace.to_address,
                            mint_transaction_hash=trace.transaction_hash,
                            mint_trace=trace.trace_address,
                            burn_transaction_hash=search_trace.transaction_hash,
                            burn_trace=search_trace.trace_address,
                            swaps=jit_swaps,
                            token0_address=transfer_info.token0_address,
                            token1_address=transfer_info.token1_address,
                            mint_token0_amount=transfer_info.mint_token0,
                            mint_token1_amount=transfer_info.mint_token1,
                            burn_token0_amount=transfer_info.burn_token0,
                            burn_token1_amount=transfer_info.burn_token1,
                            token0_swap_volume=token0_volume,
                            token1_swap_volume=token1_volume,
                        )
                    )

    return jit_liquidity_instances


def _get_token_order(token_a: str, token_b: str) -> Tuple[str, str]:
    token_order = True if int(token_a, 16) < int(token_b, 16) else False
    return (token_a, token_b) if token_order else (token_b, token_a)


def _get_swap_info(
    swaps: List[Swap],
    mint_trace: ClassifiedTrace,
    burn_trace: ClassifiedTrace,
    token0_address: str,
) -> Tuple[List[Swap], int, int]:
    jit_swaps: List[Swap] = []
    token0_swap_volume, token1_swap_volume = 0, 0

    ordered_swaps = sorted(
        swaps, key=lambda s: (s.transaction_position, s.trace_address)
    )

    for swap in ordered_swaps:
        if swap.transaction_position <= mint_trace.transaction_position:
            continue
        if swap.transaction_position >= burn_trace.transaction_position:
            break
        if swap.contract_address == mint_trace.to_address:
            jit_swaps.append(swap)
            token0_swap_volume += (
                swap.token_in_amount if swap.token_in_address == token0_address else 0
            )
            token1_swap_volume += (
                0 if swap.token_in_address == token0_address else swap.token_in_amount
            )

    return jit_swaps, token0_swap_volume, token1_swap_volume


def _get_transfer_info(
    classified_traces: List[ClassifiedTrace],
    mint_trace: ClassifiedTrace,
    burn_trace: ClassifiedTrace,
) -> JITTransferInfo:

    error_found = False
    mint_slice_start, mint_slice_end, burn_slice_start, burn_slice_end = (
        None,
        None,
        None,
        None,
    )

    for index, trace in enumerate(classified_traces):
        if (
            mint_slice_start is None
            and trace.transaction_hash == mint_trace.transaction_hash
        ):
            mint_slice_start = index
        if (
            mint_slice_end is None
            and trace.transaction_position > mint_trace.transaction_position
        ):
            mint_slice_end = index
        if (
            burn_slice_start is None
            and trace.transaction_hash == burn_trace.transaction_hash
        ):
            burn_slice_start = index
        if (
            burn_slice_end is None
            and trace.transaction_position > burn_trace.transaction_position
        ):
            burn_slice_end = index
            break

    mint_net_transfers_full = get_net_transfers(
        classified_traces[mint_slice_start:mint_slice_end]
    )
    burn_net_transfers_full = get_net_transfers(
        classified_traces[burn_slice_start:burn_slice_end]
    )

    mint_net_transfers, burn_net_transfers = [], []
    pool_address = mint_trace.to_address

    for transfer in mint_net_transfers_full:
        if transfer.to_address == pool_address:
            mint_net_transfers.append(transfer)

    for transfer in burn_net_transfers_full:
        if transfer.from_address == pool_address:
            burn_net_transfers.append(transfer)

    if len(mint_net_transfers) > 2 or len(burn_net_transfers) > 2:
        error_found = True

    if (
        len(mint_net_transfers) < 2 or len(burn_net_transfers) < 2
    ):  # Uniswap V3 Limit Case
        if len(mint_net_transfers) == 0 or len(burn_net_transfers) == 0:
            raise Exception(
                "JIT Liquidity found where no tokens are transferred to pool address"
            )

        return _parse_liquidity_limit_order(
            mint_net_transfers, burn_net_transfers, error_found
        )

    else:
        token0_address, token1_address = _get_token_order(
            mint_net_transfers[0].token_address, mint_net_transfers[1].token_address
        )

        mint_token0, mint_token1 = _parse_token_amounts(
            token0_address, mint_net_transfers
        )

        burn_token0, burn_token1 = _parse_token_amounts(
            token0_address, burn_net_transfers
        )

    return JITTransferInfo(
        token0_address=token0_address,
        token1_address=token1_address,
        mint_token0=mint_token0,
        mint_token1=mint_token1,
        burn_token0=burn_token0,
        burn_token1=burn_token1,
        error=error_found,
    )


def _get_bot_address(
    mint_trace: ClassifiedTrace,
    classified_traces: List[ClassifiedTrace],
) -> str:
    if "from_address" in mint_trace.dict().keys():

        if mint_trace.from_address in LIQUIDITY_MINT_ROUTERS:
            bot_trace = list(
                filter(
                    lambda t: t.to_address == mint_trace.from_address
                    and t.transaction_hash == mint_trace.transaction_hash,
                    classified_traces,
                )
            )
            if len(bot_trace) == 1 or is_child_trace_address(
                bot_trace[1].trace_address, bot_trace[0].trace_address
            ):
                return _get_bot_address(bot_trace[0], classified_traces)
            else:
                return ZERO_ADDRESS

        elif type(mint_trace.from_address) == str:
            return mint_trace.from_address

    return ZERO_ADDRESS


def _parse_liquidity_limit_order(
    mint_net_transfers: List[Transfer],
    burn_net_transfers: List[Transfer],
    error_found: bool,
) -> JITTransferInfo:
    try:
        token0_address, token1_address = _get_token_order(
            burn_net_transfers[0].token_address, burn_net_transfers[1].token_address
        )
    except IndexError:
        token0_address, token1_address = _get_token_order(
            mint_net_transfers[0].token_address, mint_net_transfers[1].token_address
        )

    if len(mint_net_transfers) < 2:
        if token0_address == mint_net_transfers[0].token_address:
            mint_token0 = mint_net_transfers[0].amount
            mint_token1 = 0
        else:
            mint_token0 = 0
            mint_token1 = mint_net_transfers[0].amount

        burn_token0, burn_token1 = _parse_token_amounts(
            token0_address, burn_net_transfers
        )

    else:
        if token0_address == burn_net_transfers[0].token_address:
            burn_token0 = burn_net_transfers[0].amount
            burn_token1 = 0
        else:
            burn_token0 = 0
            burn_token1 = burn_net_transfers[0].amount

        mint_token0, mint_token1 = _parse_token_amounts(
            token0_address, mint_net_transfers
        )

    return JITTransferInfo(
        token0_address=token0_address,
        token1_address=token1_address,
        mint_token0=mint_token0,
        mint_token1=mint_token1,
        burn_token0=burn_token0,
        burn_token1=burn_token1,
        error=error_found,
    )


def _parse_token_amounts(
    token0_address: str, net_transfers: List[Transfer]
) -> Tuple[int, int]:
    if token0_address == net_transfers[0].token_address:
        token0_amount = net_transfers[0].amount
        token1_amount = net_transfers[1].amount

    else:
        token0_amount = net_transfers[1].amount
        token1_amount = net_transfers[0].amount

    return token0_amount, token1_amount
