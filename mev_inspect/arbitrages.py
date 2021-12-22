from itertools import groupby
from typing import List, Optional, Tuple

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

    used_swaps: List[Swap] = []

    for (start, ends) in start_ends:
        if start in used_swaps:
            continue

        unused_ends = [end for end in ends if end not in used_swaps]
        route = _get_shortest_route(start, unused_ends, swaps)

        if route is not None:
            start_amount = route[0].token_in_amount
            end_amount = route[-1].token_out_amount
            profit_amount = end_amount - start_amount
            error = None
            for swap in route:
                if swap.error is not None:
                    error = swap.error

            arb = Arbitrage(
                swaps=route,
                block_number=route[0].block_number,
                transaction_hash=route[0].transaction_hash,
                account_address=route[0].from_address,
                profit_token_address=route[0].token_in_address,
                start_amount=start_amount,
                end_amount=end_amount,
                profit_amount=profit_amount,
                error=error,
            )

            all_arbitrages.append(arb)
            used_swaps.extend(route)

    if len(all_arbitrages) == 1:
        return all_arbitrages
    else:
        return [
            arb
            for arb in all_arbitrages
            if (arb.swaps[0].trace_address < arb.swaps[-1].trace_address)
        ]


def _get_shortest_route(
    start_swap: Swap,
    end_swaps: List[Swap],
    all_swaps: List[Swap],
) -> Optional[List[Swap]]:
    # TODO - add max length
    for end_swap in end_swaps:
        if start_swap.token_out_address == end_swap.token_in_address:
            return [start_swap, end_swap]

    other_swaps = [
        swap for swap in all_swaps if (swap is not start_swap and swap not in end_swaps)
    ]

    if len(other_swaps) == 0:
        return None

    shortest_route_rest = None

    for next_swap in other_swaps:
        if start_swap.token_out_address == next_swap.token_in_address and (
            start_swap.contract_address == next_swap.from_address
            or start_swap.to_address == next_swap.contract_address
            or start_swap.to_address == next_swap.from_address
        ):
            shortest_from_next = _get_shortest_route(
                next_swap,
                end_swaps,
                other_swaps,
            )

            if shortest_from_next is not None and (
                shortest_route_rest is None
                or len(shortest_from_next) < len(shortest_route_rest)
            ):
                shortest_route_rest = shortest_from_next

    if shortest_route_rest is None:
        return None
    else:
        return [start_swap] + shortest_route_rest


def _get_all_start_end_swaps(swaps: List[Swap]) -> List[Tuple[Swap, List[Swap]]]:
    """
    Gets the set of all possible opening and closing swap pairs in an arbitrage via
    - swap[start].token_in == swap[end].token_out
    - swap[start].from_address == swap[end].to_address
    - not swap[start].from_address in all_pool_addresses
    - not swap[end].to_address in all_pool_addresses
    """
    pool_addrs = [swap.contract_address for swap in swaps]
    valid_start_ends: List[Tuple[Swap, List[Swap]]] = []

    for index, potential_start_swap in enumerate(swaps):
        ends_for_start: List[Swap] = []
        remaining_swaps = swaps[:index] + swaps[index + 1 :]

        for potential_end_swap in remaining_swaps:
            if (
                potential_start_swap.token_in_address
                == potential_end_swap.token_out_address
                and potential_start_swap.from_address == potential_end_swap.to_address
                and not potential_start_swap.from_address in pool_addrs
            ):

                ends_for_start.append(potential_end_swap)

        if len(ends_for_start) > 0:
            valid_start_ends.append((potential_start_swap, ends_for_start))

    return valid_start_ends
