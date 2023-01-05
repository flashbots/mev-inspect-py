import json
from typing import List

from mev_inspect.models.liquidations import LiquidationModel
from mev_inspect.schemas.liquidations import Liquidation

from .shared import delete_by_block_range


def delete_liquidations_for_blocks(
    db_session,
    after_block_number: int,
    before_block_number: int,
) -> None:
    delete_by_block_range(
        db_session,
        LiquidationModel,
        after_block_number,
        before_block_number,
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
    # db_session.commit()
