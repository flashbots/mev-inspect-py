from typing import List

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

    for index, front_swap in enumerate(ordered_swaps):
        sandwicher_address = front_swap.from_address
        rest_swaps = ordered_swaps[index:]

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
                    sandwiches.append(
                        Sandwich(
                            block_number=front_swap.block_number,
                            sandwicher_address=sandwicher_address,
                            frontrun_transaction_hash=front_swap.transaction_hash,
                            backrun_transaction_hash=other_swap.transaction_hash,
                            sandwiched_swaps=sandwiched_swaps,
                        )
                    )

                    break

    return sandwiches
