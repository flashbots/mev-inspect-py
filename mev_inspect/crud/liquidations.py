import json
from typing import List

from mev_inspect.models.liquidations import LiquidationModel
from mev_inspect.schemas.liquidations import Liquidation


async def delete_liquidations_for_block(
    db_session,
    block_number: int,
) -> None:
    await (
        db_session.query(LiquidationModel)
        .filter(LiquidationModel.block_number == block_number)
        .delete()
    )

    await db_session.commit()


async def write_liquidations(
    db_session,
    liquidations: List[Liquidation],
) -> None:
    models = [
        LiquidationModel(**json.loads(liquidation.json()))
        for liquidation in liquidations
    ]

    await db_session.bulk_save_objects(models)
    await db_session.commit()
