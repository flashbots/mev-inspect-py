from typing import List

from mev_inspect.crud.generic import delete_by_block_number, write_models
from mev_inspect.models.miner_payments import MinerPaymentModel
from mev_inspect.schemas.miner_payments import MinerPayment


async def delete_miner_payments_for_block(db_session, block_number: int) -> None:
    await delete_by_block_number(
        db_session=db_session, block_number=block_number, model=MinerPaymentModel
    )


async def write_miner_payments(db_session, miner_payments: List[MinerPayment]) -> None:
    await write_models(db_session, miner_payments, MinerPaymentModel)
