from typing import List, Optional

from mev_inspect.schemas.sandwiches import Sandwich
from mev_inspect.schemas.swaps import Swap


def get_sandwiches(swaps: List[Swap]) -> List[Sandwich]:
    ordered_swaps = list(
        sorted(
            swaps,
            key=lambda swap: (swap.transaction_position, swap.trace_address),
        )
    )

    sandwiches: List[Sandwich] = []

    for index, swap in enumerate(ordered_swaps):
        rest_swaps = ordered_swaps[index + 1 :]
        sandwich = _get_sandwich_starting_with_swap(swap, rest_swaps)

        if sandwich is not None:
            sandwiches.append(sandwich)

    return sandwiches


def _get_sandwich_starting_with_swap(
    front_swap: Swap,
    rest_swaps: List[Swap],
) -> Optional[Sandwich]:

    sandwicher_address = front_swap.from_address
    sandwiched_swaps = []

    for other_swap in rest_swaps:
        if other_swap.transaction_hash == front_swap.transaction_hash:
            continue

        if other_swap.contract_address == front_swap.contract_address:
            if (
                other_swap.token_in_address == front_swap.token_in_address
                and other_swap.token_out_address == front_swap.token_out_address
                and other_swap.from_address != sandwicher_address
            ):
                sandwiched_swaps.append(other_swap)
            elif (
                other_swap.token_out_address == front_swap.token_in_address
                and other_swap.token_in_address == front_swap.token_out_address
                and other_swap.from_address == sandwicher_address
            ):
                return Sandwich(
                    block_number=front_swap.block_number,
                    sandwicher_address=sandwicher_address,
                    frontrun_swap=front_swap,
                    backrun_swap=other_swap,
                    sandwiched_swaps=sandwiched_swaps,
                )

    return None
