from itertools import groupby
from typing import List, Tuple

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
    """
    An arbitrage is defined as multiple swaps in a series that result in the initial token being returned
    to the initial sender address.

    There are 2 types of swaps that are most common (99%+).
    Case I (fully routed):
    BOT -> A/B -> B/C -> C/A -> BOT

    Case II (always return to bot):
    BOT -> A/B -> BOT -> B/C -> BOT -> A/C -> BOT

    There is only 1 correct way to route Case I, but for Case II the following valid routes could be found:
    A->B->C->A / B->C->A->B / C->A->B->C. Thus when multiple valid routes are found we filter to the set that
    happen in valid order.
    """

    all_arbitrages = []

    start_ends = _get_all_start_end_swaps(swaps)
    if len(start_ends) == 0:
        return []

    # for (start, end) in filtered_start_ends:
    for (start, end) in start_ends:
        potential_intermediate_swaps = [
            swap for swap in swaps if swap is not start and swap is not end
        ]
        routes = _get_all_routes(start, end, potential_intermediate_swaps)

        for route in routes:
            start_amount = route[0].token_in_amount
            end_amount = route[-1].token_out_amount
            profit_amount = end_amount - start_amount

            arb = Arbitrage(
                swaps=route,
                block_number=route[0].block_number,
                transaction_hash=route[0].transaction_hash,
                account_address=route[0].from_address,
                profit_token_address=route[0].token_in_address,
                start_amount=start_amount,
                end_amount=end_amount,
                profit_amount=profit_amount,
            )
            all_arbitrages.append(arb)
    if len(all_arbitrages) == 1:
        return all_arbitrages
    else:
        return [
            arb
            for arb in all_arbitrages
            if (arb.swaps[0].trace_address < arb.swaps[-1].trace_address)
        ]


def _get_all_start_end_swaps(swaps: List[Swap]) -> List[Tuple[Swap, Swap]]:
    """
    Gets the set of all possible opening and closing swap pairs in an arbitrage via
    - swap[start].token_in == swap[end].token_out
    - swap[start].from_address == swap[end].to_address
    - not swap[start].from_address in all_pool_addresses
    - not swap[end].to_address in all_pool_addresses
    """
    pool_addrs = [swap.contract_address for swap in swaps]
    valid_start_ends: List[Tuple[Swap, Swap]] = []
    for index, potential_start_swap in enumerate(swaps):
        remaining_swaps = swaps[:index] + swaps[index + 1 :]
        for potential_end_swap in remaining_swaps:
            if (
                potential_start_swap.token_in_address
                == potential_end_swap.token_out_address
                and potential_start_swap.from_address == potential_end_swap.to_address
                and not potential_start_swap.from_address in pool_addrs
            ):
                valid_start_ends.append((potential_start_swap, potential_end_swap))
    return valid_start_ends


def _get_all_routes(
    start_swap: Swap, end_swap: Swap, other_swaps: List[Swap]
) -> List[List[Swap]]:
    """
    Returns all routes (List[Swap]) from start to finish between a start_swap and an end_swap only accounting for token_address_in and token_address_out.
    """
    # If the path is complete, return
    if start_swap.token_out_address == end_swap.token_in_address:
        return [[start_swap, end_swap]]
    elif len(other_swaps) == 0:
        return []

    # Collect all potential next steps, check if valid, recursively find routes from next_step to end_swap
    routes: List[List[Swap]] = []
    for potential_next_swap in other_swaps:
        if start_swap.token_out_address == potential_next_swap.token_in_address and (
            start_swap.contract_address == potential_next_swap.from_address
            or start_swap.to_address == potential_next_swap.contract_address
            or start_swap.to_address == potential_next_swap.from_address
        ):
            remaining_swaps = [
                swap for swap in other_swaps if swap != potential_next_swap
            ]
            next_swap_routes = _get_all_routes(
                potential_next_swap, end_swap, remaining_swaps
            )
            if len(next_swap_routes) > 0:
                for next_swap_route in next_swap_routes:
                    next_swap_route.insert(0, start_swap)
                    routes.append(next_swap_route)
    return routes
