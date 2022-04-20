from typing import List

from mev_inspect.schemas.jit_liquidity import JITLiquidity
from mev_inspect.schemas.swaps import Swap
from mev_inspect.schemas.transfers import Transfer
from mev_inspect.transfers import get_net_transfers
from mev_inspect.traces import is_child_trace_address
from mev_inspect.schemas.traces import ClassifiedTrace, DecodedCallTrace, Classification, Protocol

LIQUIDITY_MINT_ROUTERS = [
    "0xC36442b4a4522E871399CD717aBDD847Ab11FE88".lower(),  # Uniswap V3 NFT Position Manager
]


def get_jit_liquidity(
        classified_traces: List[ClassifiedTrace],
        swaps: List[Swap]
) -> List[JITLiquidity]:
    jit_liquidity_instances: List[JITLiquidity] = []

    for index, trace in enumerate(classified_traces):

        if not isinstance(trace, DecodedCallTrace):
            continue

        if trace.classification == Classification.liquidity_mint and trace.protocol == Protocol.uniswap_v3:
            i = index + 1
            while i < len(classified_traces):
                forward_search_trace = classified_traces[i]
                if forward_search_trace.classification == Classification.liquidity_burn:
                    if forward_search_trace.to_address == trace.to_address:
                        jit_liquidity_instances.append(
                            _parse_jit_liquidity_instance(trace, forward_search_trace, classified_traces, swaps)
                        )
                i += 1

    return jit_liquidity_instances


def _parse_jit_liquidity_instance(
        mint_trace: ClassifiedTrace,
        burn_trace: ClassifiedTrace,
        classified_traces: List[ClassifiedTrace],
        swaps: List[Swap],
) -> JITLiquidity:
    valid_swaps = list(filter(
        lambda t: mint_trace.transaction_position < t.transaction_position < burn_trace.transaction_position,
        swaps
    ))
    net_transfers = get_net_transfers(list(filter(
        lambda t: t.transaction_hash in [mint_trace.transaction_hash, burn_trace.transaction_hash],
        classified_traces)))

    jit_swaps: List[Swap] = []
    token0_swap_volume, token1_swap_volume = 0, 0

    mint_transfers: List[Transfer] = list(filter(
        lambda t: t.transaction_hash == mint_trace.transaction_hash and t.to_address == mint_trace.to_address,
        net_transfers))
    burn_transfers: List[Transfer] = list(filter(
        lambda t: t.transaction_hash == burn_trace.transaction_hash and t.from_address == burn_trace.to_address,
        net_transfers))

    if len(mint_transfers) == 2 and len(burn_transfers) == 2:
        token0_address, token1_address = _get_token_order(mint_transfers[0].token_address,
                                                          mint_transfers[1].token_address)
    else:
        # This is a failing/skipping case, super weird
        return None

    bot_address = _get_bot_address(mint_trace, classified_traces)
    for swap in valid_swaps:
        if swap.contract_address == mint_trace.to_address:
            jit_swaps.append(swap)
            token0_swap_volume += swap.token_in_amount if swap.token_in_address == token0_address else 0
            token1_swap_volume += 0 if swap.token_in_address == token0_address else swap.token_in_amount

    return JITLiquidity(
        block_number=mint_trace.block_number,
        bot_address=bot_address,
        pool_address=mint_trace.to_address,
        mint_transaction_hash=mint_trace.transaction_hash,
        mint_trace=mint_trace.trace_address,
        burn_transaction_hash=burn_trace.transaction_hash,
        burn_trace=burn_trace.trace_address,
        swaps=jit_swaps,
        token0_address=token0_address,
        token1_address=token1_address,
        mint_token0_amount=mint_transfers[0].amount if mint_transfers[0].token_address == token0_address else mint_transfers[1].amount,
        mint_token1_amount=mint_transfers[1].amount if mint_transfers[0].token_address == token0_address else mint_transfers[0].amount,
        burn_token0_amount=burn_transfers[0].amount if burn_transfers[0].token_address == token0_address else burn_transfers[1].amount,
        burn_token1_amount=burn_transfers[1].amount if burn_transfers[0].token_address == token0_address else burn_transfers[0].amount,
        token0_swap_volume=token0_swap_volume,
        token1_swap_volume=token1_swap_volume,
    )


def _get_token_order(token_a: str, token_b: str) -> (int, int):
    token_order = True if int(token_a, 16) < int(token_b, 16) else False
    return (token_a, token_b) if token_order else (token_b, token_a)


def _get_bot_address(
        mint_trace: ClassifiedTrace,
        classified_traces: List[ClassifiedTrace]
) -> str:
    if mint_trace.from_address not in LIQUIDITY_MINT_ROUTERS:
        return mint_trace.from_address

    bot_trace = list(filter(
        lambda t: t.to_address == mint_trace.from_address and t.transaction_hash == mint_trace.transaction_hash,
        classified_traces
    ))
    if len(bot_trace) > 1:
        if is_child_trace_address(bot_trace[1].trace_address, bot_trace[0].trace_address):
            return _get_bot_address(bot_trace[0], classified_traces)
        else:
            return "0x" + ("0" * 40)  # get rid of this case by properly searching the trace_address
    _get_bot_address(bot_trace[0], classified_traces)


