import json
from typing import List

from mev_inspect.models.miner_payments import MinerPaymentModel
from mev_inspect.schemas.miner_payments import MinerPayment

from .shared import delete_by_block_range


def delete_miner_payments_for_blocks(
    db_session,
    after_block_number: int,
    before_block_number: int,
) -> None:
    delete_by_block_range(
        db_session,
        MinerPaymentModel,
        after_block_number,
        before_block_number,
    )
    db_session.commit()


def write_miner_payments(
    db_session,
    miner_payments: List[MinerPayment],
) -> None:
    models = [
        MinerPaymentModel(**json.loads(miner_payment.json()))
        for miner_payment in miner_payments
    ]

    db_session.bulk_save_objects(models)
    db_session.commit()
