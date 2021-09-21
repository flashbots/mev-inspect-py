from itertools import groupby
from typing import List
from functools import cmp_to_key

from mev_inspect.schemas.arbitrages import Arbitrage
from mev_inspect.schemas.swaps import Swap


def get_arbitrages(swaps: List[Swap]) -> List[Arbitrage]:
    get_transaction_hash = lambda swap: swap.transaction_hash
    swaps_by_transaction = groupby(
        sorted(swaps, key=get_transaction_hash),
        key=get_transaction_hash,
    )

    all_arbitrages = []

    for _, transaction_swaps in swaps_by_transaction:
        all_arbitrages += _get_arbitrages_from_swaps(
            list(transaction_swaps),
        )

    return all_arbitrages


def _get_arbitrages_from_swaps(swaps: List[Swap]) -> List[Arbitrage]:
    all_arbitrages = []

    ordered_swaps = _order_swaps_by_trace_order(swaps)

    grouped_swaps: List[List[Swap]] = []

    # An arbitrage is defined as multiple swaps in a row that result in the initial token being returned.
    # Ex: [WETH -> UNI, UNI -> DAI, DAI -> WETH]
    # Code below assumes there can be multiple arbitrages per swap set, but they'll be serial.
    # Ex: [WETH -> UNI, UNI -> WETH, DAI -> SUSHI, SUSHI -> DAI]
    # Non-working ex: [WETH -> UNI, DAI -> SUSHI, UNI -> WETH, SUSHI -> DAI]
    for start_swap_index in range(len(ordered_swaps)):
        current_swap = ordered_swaps[start_swap_index]
        swap_path: List[Swap] = [current_swap]

        for path_index in range(start_swap_index + 1, len(ordered_swaps)):
            next_swap = ordered_swaps[path_index]
            if current_swap.token_out_address == next_swap.token_in_address:
                swap_path.append(next_swap)
                current_swap = next_swap
                if (
                    swap_path[0].token_in_address == next_swap.token_out_address
                ):  # Cycle complete
                    grouped_swaps.append(swap_path)
                    swap_path = []
            else:
                swap_path = []

    for swap_path in grouped_swaps:
        start_amount = swap_path[0].token_in_amount
        end_amount = swap_path[-1].token_out_amount
        profit_amount = end_amount - start_amount

        arb = Arbitrage(
            swaps=swap_path,
            block_number=swap_path[0].block_number,
            transaction_hash=swap_path[0].transaction_hash,
            account_address=swap_path[0].from_address,
            profit_token_address=swap_path[0].token_in_address,
            start_amount=start_amount,
            end_amount=end_amount,
            profit_amount=profit_amount,
        )
        all_arbitrages.append(arb)

    return all_arbitrages


def _order_swaps_by_trace_order(unordered_swaps: List[Swap]) -> List[Swap]:
    unordered_swaps.sort(key=cmp_to_key(_compare_trace_address))
    return unordered_swaps


def _compare_trace_address(a: Swap, b: Swap):
    if a.trace_address == b.trace_address:
        return 0
    for i in range(0, max(len(a.trace_address), len(b.trace_address))):
        if len(a.trace_address) == i:
            return -1
        if len(b.trace_address) == i:
            return 1

        if a.trace_address[i] > b.trace_address[i]:
            return 1
        if a.trace_address[i] < b.trace_address[i]:
            return -1
    return 0
