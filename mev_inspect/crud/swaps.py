from typing import List

from mev_inspect.crud.generic import delete_by_block_number, write_models
from mev_inspect.models.swaps import SwapModel
from mev_inspect.schemas.swaps import Swap


async def delete_swaps_for_block(db_session, block_number: int) -> None:
    await delete_by_block_number(
        db_session=db_session, block_number=block_number, model=SwapModel
    )


async def write_swaps(db_session, swaps: List[Swap]) -> None:
    await write_models(db_session, swaps, SwapModel)
