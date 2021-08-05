from typing import List
from uuid import uuid4

from mev_inspect.models.arbitrages import ArbitrageModel
from mev_inspect.schemas.arbitrages import Arbitrage


def delete_arbitrages_for_block(
    db_session,
    block_number: int,
) -> None:
    (
        db_session.query(ArbitrageModel)
        .filter(ArbitrageModel.block_number == block_number)
        .delete()
    )

    db_session.commit()


def write_arbitrages(
    db_session,
    arbitrages: List[Arbitrage],
) -> None:
    arbitrage_models = [
        ArbitrageModel(
            id=str(uuid4()),
            block_number=arbitrage.block_number,
            transaction_hash=arbitrage.transaction_hash,
            account_address=arbitrage.account_address,
            profit_token_address=arbitrage.profit_token_address,
            start_amount=arbitrage.start_amount,
            end_amount=arbitrage.end_amount,
            profit_amount=arbitrage.profit_amount,
        )
        for arbitrage in arbitrages
    ]

    db_session.bulk_save_objects(arbitrage_models)
    db_session.commit()
