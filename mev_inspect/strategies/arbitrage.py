from itertools import groupby
from typing import List, Optional

from mev_inspect.schemas.arbitrage import Arbitrage
from mev_inspect.schemas.classified_traces import ClassifiedTrace
from mev_inspect.schemas.swaps import Swap
from mev_inspect.swaps import get_swaps


UNISWAP_V2_PAIR_ABI_NAME = "UniswapV2Pair"
UNISWAP_V3_POOL_ABI_NAME = "UniswapV3Pool"


def get_arbitrages(traces: List[ClassifiedTrace]) -> List[Arbitrage]:
    get_transaction_hash = lambda t: t.transaction_hash
    traces_by_transaction = groupby(
        sorted(traces, key=get_transaction_hash),
        key=get_transaction_hash,
    )

    all_arbitrages = []

    for _, transaction_traces in traces_by_transaction:
        all_arbitrages += _get_arbitrages_for_transaction(
            list(transaction_traces),
        )

    return all_arbitrages


def _get_arbitrages_for_transaction(
    traces: List[ClassifiedTrace],
) -> List[Arbitrage]:
    swaps = get_swaps(traces)

    if len(swaps) > 1:
        return _get_arbitrages_from_swaps(swaps)

    return []


def _get_arbitrages_from_swaps(swaps: List[Swap]) -> List[Arbitrage]:
    pool_addresses = {swap.pool_address for swap in swaps}

    all_arbitrages = []

    for index, first_swap in enumerate(swaps):
        other_swaps = swaps[:index] + swaps[index + 1 :]

        if first_swap.from_address not in pool_addresses:
            arbitrage = _get_arbitrage_starting_with_swap(first_swap, other_swaps)

            if arbitrage is not None:
                all_arbitrages.append(arbitrage)

    return all_arbitrages


def _get_arbitrage_starting_with_swap(
    start_swap: Swap,
    other_swaps: List[Swap],
) -> Optional[Arbitrage]:
    swap_path = [start_swap]

    current_address = start_swap.to_address
    current_token = start_swap.token_out_address

    while True:
        swaps_from_current_address = []

        for swap in other_swaps:
            if (
                swap.pool_address == current_address
                and swap.token_in_address == current_token
            ):
                swaps_from_current_address.append(swap)

        if len(swaps_from_current_address) == 0:
            return None

        if len(swaps_from_current_address) > 1:
            raise RuntimeError("todo")

        latest_swap = swaps_from_current_address[0]
        swap_path.append(latest_swap)

        current_address = latest_swap.to_address
        current_token = latest_swap.token_out_address

        if (
            current_address == start_swap.from_address
            and current_token == start_swap.token_in_address
        ):

            start_amount = start_swap.token_in_amount
            end_amount = latest_swap.token_out_amount
            profit_amount = end_amount - start_amount

            return Arbitrage(
                swaps=swap_path,
                account_address=start_swap.from_address,
                profit_token_address=start_swap.token_in_address,
                start_amount=start_amount,
                end_amount=end_amount,
                profit_amount=profit_amount,
            )

    return None
