import json
from typing import List

from mev_inspect.models.swaps import SwapModel
from mev_inspect.schemas.swaps import Swap

from .shared import delete_by_block_range


def delete_swaps_for_blocks(
    db_session,
    after_block_number: int,
    before_block_number: int,
) -> None:
    delete_by_block_range(
        db_session,
        SwapModel,
        after_block_number,
        before_block_number,
    )
    db_session.commit()


def write_swaps(
    db_session,
    swaps: List[Swap],
) -> None:
    models = [SwapModel(**json.loads(swap.json())) for swap in swaps]

    db_session.bulk_save_objects(models)
    # db_session.commit()
