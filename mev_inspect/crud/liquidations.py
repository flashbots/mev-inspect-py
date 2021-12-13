import json

from typing import List

from mev_inspect.models.liquidations import LiquidationModel
from mev_inspect.schemas.liquidations import Liquidation


def delete_liquidations_for_block(
    db_session,
    block_number: int,
) -> None:
    (
        db_session.query(LiquidationModel)
        .filter(LiquidationModel.block_number == block_number)
        .delete()
    )

    db_session.commit()


def write_liquidations(
    db_session,
    liquidations: List[Liquidation],
) -> None:
    models = [
        LiquidationModel(**json.loads(liquidation.json()))
        for liquidation in liquidations
    ]

    db_session.bulk_save_objects(models)
    db_session.commit()
