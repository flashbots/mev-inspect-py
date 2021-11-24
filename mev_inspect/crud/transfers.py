from typing import Sequence

from mev_inspect.crud.generic import delete_by_block_number, write_models
from mev_inspect.models.transfers import TransferModel
from mev_inspect.schemas.transfers import Transfer


async def delete_transfers_for_block(db_session, block_number: int) -> None:
    await delete_by_block_number(
        db_session=db_session, block_number=block_number, model=TransferModel
    )


async def write_transfers(db_session, transfers: Sequence[Transfer]) -> None:
    await write_models(db_session, transfers, TransferModel)
