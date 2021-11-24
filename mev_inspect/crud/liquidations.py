from typing import List

from mev_inspect.crud.generic import delete_by_block_number, write_models
from mev_inspect.models.liquidations import LiquidationModel
from mev_inspect.schemas.liquidations import Liquidation


async def delete_liquidations_for_block(db_session, block_number: int) -> None:
    await delete_by_block_number(
        db_session=db_session, block_number=block_number, model=LiquidationModel
    )


async def write_liquidations(db_session, liquidations: List[Liquidation]) -> None:
    await write_models(db_session, liquidations, LiquidationModel)
