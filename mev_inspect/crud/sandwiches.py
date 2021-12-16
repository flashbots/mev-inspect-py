from typing import List
from uuid import uuid4

from mev_inspect.models.sandwiches import SandwichModel
from mev_inspect.schemas.sandwiches import Sandwich


def delete_sandwiches_for_block(
    db_session,
    block_number: int,
) -> None:
    (
        db_session.query(SandwichModel)
        .filter(SandwichModel.block_number == block_number)
        .delete()
    )

    db_session.commit()


def write_sandwiches(
    db_session,
    sandwiches: List[Sandwich],
) -> None:
    sandwich_models = []
    sandwiched_swaps = []

    for sandwich in sandwiches:
        sandwich_id = str(uuid4())
        sandwich_models.append(
            SandwichModel(
                id=sandwich_id,
                block_number=sandwich.block_number,
                sandwicher_address=sandwich.sandwicher_address,
                frontrun_swap_transaction_hash=sandwich.frontrun_swap.transaction_hash,
                frontrun_swap_trace_address=sandwich.frontrun_swap.trace_address,
                backrun_swap_transaction_hash=sandwich.backrun_swap.transaction_hash,
                backrun_swap_trace_address=sandwich.backrun_swap.trace_address,
            )
        )

        for swap in sandwich.sandwiched_swaps:
            sandwiched_swaps.append(
                {
                    "sandwich_id": sandwich_id,
                    "block_number": swap.block_number,
                    "transaction_hash": swap.transaction_hash,
                    "trace_address": swap.trace_address,
                }
            )

    if len(sandwich_models) > 0:
        db_session.bulk_save_objects(sandwich_models)
        db_session.execute(
            """
            INSERT INTO sandwiched_swaps
            (sandwich_id, block_number, transaction_hash, trace_address)
            VALUES
            (:sandwich_id, :block_number, :transaction_hash, :trace_address)
            """,
            params=sandwiched_swaps,
        )

        db_session.commit()
