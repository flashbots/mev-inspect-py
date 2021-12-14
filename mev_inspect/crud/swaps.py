import json
from typing import List

from mev_inspect.models.swaps import SwapModel
from mev_inspect.schemas.swaps import Swap


def delete_swaps_for_block(
    db_session,
    block_number: int,
) -> None:
    (
        db_session.query(SwapModel)
        .filter(SwapModel.block_number == block_number)
        .delete()
    )

    db_session.commit()


def write_swaps(
    db_session,
    swaps: List[Swap],
) -> None:
    models = [SwapModel(**json.loads(swap.json())) for swap in swaps]

    db_session.bulk_save_objects(models)
    db_session.commit()
