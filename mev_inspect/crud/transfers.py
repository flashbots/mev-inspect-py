import json
from typing import List

from mev_inspect.models.transfers import TransferModel
from mev_inspect.schemas.transfers import Transfer

from .shared import delete_by_block_range


def delete_transfers_for_blocks(
    db_session,
    after_block_number: int,
    before_block_number: int,
) -> None:
    delete_by_block_range(
        db_session,
        TransferModel,
        after_block_number,
        before_block_number,
    )

    db_session.commit()


def write_transfers(
    db_session,
    transfers: List[Transfer],
) -> None:
    models = [TransferModel(**json.loads(transfer.json())) for transfer in transfers]

    db_session.bulk_save_objects(models)
    db_session.commit()
