import json
from typing import List

from mev_inspect.models.transfers import TransferModel
from mev_inspect.schemas.transfers import ERC20Transfer


def delete_transfers_for_block(
    db_session,
    block_number: int,
) -> None:
    (
        db_session.query(TransferModel)
        .filter(TransferModel.block_number == block_number)
        .delete()
    )

    db_session.commit()


def write_transfers(
    db_session,
    transfers: List[ERC20Transfer],
) -> None:
    models = [TransferModel(**json.loads(transfer.json())) for transfer in transfers]

    db_session.bulk_save_objects(models)
    db_session.commit()
