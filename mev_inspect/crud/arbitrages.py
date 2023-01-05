from typing import List
from uuid import uuid4

from mev_inspect.models.arbitrages import ArbitrageModel
from mev_inspect.schemas.arbitrages import Arbitrage

from .shared import delete_by_block_range


def delete_arbitrages_for_blocks(
    db_session,
    after_block_number: int,
    before_block_number: int,
) -> None:
    delete_by_block_range(
        db_session,
        ArbitrageModel,
        after_block_number,
        before_block_number,
    )
    db_session.commit()


def write_arbitrages(
    db_session,
    arbitrages: List[Arbitrage],
) -> None:
    arbitrage_models = []
    swap_arbitrage_ids = []

    for arbitrage in arbitrages:
        arbitrage_id = str(uuid4())
        arbitrage_models.append(
            ArbitrageModel(
                id=arbitrage_id,
                block_number=arbitrage.block_number,
                transaction_hash=arbitrage.transaction_hash,
                account_address=arbitrage.account_address,
                profit_token_address=arbitrage.profit_token_address,
                start_amount=arbitrage.start_amount,
                end_amount=arbitrage.end_amount,
                profit_amount=arbitrage.profit_amount,
                error=arbitrage.error,
                protocols={
                    swap.protocol.value
                    for swap in arbitrage.swaps
                    if swap.protocol is not None
                },
            )
        )

        for swap in arbitrage.swaps:
            swap_arbitrage_ids.append(
                {
                    "arbitrage_id": arbitrage_id,
                    "swap_transaction_hash": swap.transaction_hash,
                    "swap_trace_address": swap.trace_address,
                }
            )

    if len(arbitrage_models) > 0:
        db_session.bulk_save_objects(arbitrage_models)
        db_session.execute(
            """
            INSERT INTO arbitrage_swaps
            (arbitrage_id, swap_transaction_hash, swap_trace_address)
            VALUES
            (:arbitrage_id, :swap_transaction_hash, :swap_trace_address)
            """,
            params=swap_arbitrage_ids,
        )

        # db_session.commit()
