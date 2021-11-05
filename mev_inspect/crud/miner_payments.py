import json
from typing import List

from mev_inspect.models.miner_payments import MinerPaymentModel
from mev_inspect.schemas.miner_payments import MinerPayment


async def delete_miner_payments_for_block(
    db_session,
    block_number: int,
) -> None:
    await (
        db_session.query(MinerPaymentModel)
        .filter(MinerPaymentModel.block_number == block_number)
        .delete()
    )

    await db_session.commit()


async def write_miner_payments(
    db_session,
    miner_payments: List[MinerPayment],
) -> None:
    models = [
        MinerPaymentModel(**json.loads(miner_payment.json()))
        for miner_payment in miner_payments
    ]

    await db_session.bulk_save_objects(models)
    await db_session.commit()
