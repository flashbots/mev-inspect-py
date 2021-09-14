import json
from typing import List, Optional

from sqlalchemy.sql.expression import func

from mev_inspect.models.miner_payments import MinerPaymentModel
from mev_inspect.schemas.miner_payments import MinerPayment


def delete_miner_payments_for_block(
    db_session,
    block_number: int,
) -> None:
    (
        db_session.query(MinerPaymentModel)
        .filter(MinerPaymentModel.block_number == block_number)
        .delete()
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


def get_max_miner_payment_block(db_session) -> Optional[int]:
    results = db_session.query(func.max(MinerPaymentModel.block_number)).one_or_none()
    if results is None:
        return None
    else:
        return int(results[0])
