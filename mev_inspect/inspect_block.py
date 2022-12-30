import logging
from typing import Any, Dict, List

from sqlalchemy import orm
from web3 import Web3

from mev_inspect.arbitrages import get_arbitrages
from mev_inspect.block import get_classified_traces_from_events
from mev_inspect.crud.total_profits import write_total_profits_for_blocks
from mev_inspect.schemas.total_profits import TotalProfits

logger = logging.getLogger(__name__)

TRAILING_ZEROS = "000000000000000000000000"


async def inspect_block(
    inspect_db_session: orm.Session,
    w3: Web3,
    block_number: int,
):
    await inspect_many_blocks(
        inspect_db_session,
        w3,
        block_number,
        block_number + 1,
    )


async def inspect_many_blocks(
    inspect_db_session: orm.Session,
    w3: Web3,
    after_block_number: int,
    before_block_number: int,
):
    count = 0
    arbitrages_payload = []
    liquidations_payload = []

    profits: List[TotalProfits] = []
    async for swaps, liquidations in get_classified_traces_from_events(
        w3, after_block_number, before_block_number
    ):
        arbitrages = get_arbitrages(swaps)

        if len(arbitrages) > 0:
            for arb in arbitrages:
                arb_payload: Dict[str, Any] = dict()
                arb_payload["block_number"] = arb.block_number
                arb_payload["transaction"] = arb.transaction_hash
                arb_payload["account"] = arb.account_address
                arb_payload["profit_amt"] = arb.profit_amount
                arb_payload["token"] = arb.profit_token_address
                arbitrages_payload.append(arb_payload)
                count += 1
                profits.append(
                    TotalProfits(
                        block_number=arb.block_number,
                        transaction_hash=arb.transaction_hash,
                        token_debt="",
                        amount_debt=0,
                        token_received=str(arb.profit_token_address).replace(
                            TRAILING_ZEROS, ""
                        ),
                        amount_received=arb.profit_amount,
                    )
                )

        if len(liquidations) > 0:
            for liq in liquidations:
                liq_payload: Dict[str, Any] = dict()
                liq_payload["block_number"] = liq.block_number
                liq_payload["transaction"] = liq.transaction_hash
                liq_payload["liquidator"] = liq.liquidator_user
                liq_payload["purchase_addr"] = liq.debt_token_address
                liq_payload["receive_addr"] = liq.received_token_address
                liq_payload["purchase_amount"] = liq.debt_purchase_amount
                liq_payload["receive_amount"] = liq.received_amount
                liquidations_payload.append(liq_payload)
                count += 1
                profits.append(
                    TotalProfits(
                        block_number=liq.block_number,
                        transaction_hash=liq.transaction_hash,
                        token_debt=str(liq.debt_token_address).replace(
                            TRAILING_ZEROS, ""
                        ),
                        amount_debt=liq.debt_purchase_amount,
                        token_received=str(liq.received_amount).replace(
                            TRAILING_ZEROS, ""
                        ),
                        amount_received=liq.received_amount,
                    )
                )

    if count > 0:
        print("writing profits of {0} mev transactions".format(count))
        write_total_profits_for_blocks(
            inspect_db_session=inspect_db_session, total_profits_for_blocks=profits
        )
        arbitrages_payload = []
        liquidations_payload = []
        count = 0
