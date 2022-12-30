import json
from typing import List

from mev_inspect.models.total_profits import TotalProfitsModel
from mev_inspect.schemas.total_profits import TotalProfits


def write_total_profits_for_blocks(
    inspect_db_session,
    total_profits_for_blocks: List[TotalProfits],
) -> None:
    models = [
        TotalProfitsModel(**json.loads(swap.json()))
        for swap in total_profits_for_blocks
    ]

    inspect_db_session.bulk_save_objects(models)
    inspect_db_session.commit()
