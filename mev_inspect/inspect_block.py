import logging
from typing import Optional

from sqlalchemy import orm
from web3 import Web3

from mev_inspect.arbitrages import get_arbitrages
from mev_inspect.block import create_from_block_number
from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.crud.arbitrages import (
    delete_arbitrages_for_block,
    write_arbitrages,
)
from mev_inspect.crud.traces import (
    delete_classified_traces_for_block,
    write_classified_traces,
)
from mev_inspect.crud.miner_payments import (
    delete_miner_payments_for_block,
    write_miner_payments,
)

from mev_inspect.crud.swaps import delete_swaps_for_block, write_swaps
from mev_inspect.crud.transfers import delete_transfers_for_block, write_transfers
from mev_inspect.crud.liquidations import (
    delete_liquidations_for_block,
    write_liquidations,
)
from mev_inspect.miner_payments import get_miner_payments
from mev_inspect.punks import get_punk_bid_acceptances, get_punk_bids, get_punk_snipes
from mev_inspect.swaps import get_swaps
from mev_inspect.transfers import get_transfers
from mev_inspect.liquidations import get_liquidations


logger = logging.getLogger(__name__)


async def inspect_block(
    inspect_db_session: orm.Session,
    base_provider,
    w3: Web3,
    trace_clasifier: TraceClassifier,
    block_number: int,
    trace_db_session: Optional[orm.Session],
    should_write_classified_traces: bool = True,
):
    block = await create_from_block_number(
        base_provider,
        w3,
        block_number,
        trace_db_session,
    )

    logger.info(f"Block: {block_number} -- Total traces: {len(block.traces)}")

    total_transactions = len(
        set(t.transaction_hash for t in block.traces if t.transaction_hash is not None)
    )
    logger.info(f"Block: {block_number} -- Total transactions: {total_transactions}")

    classified_traces = trace_clasifier.classify(block.traces)
    logger.info(
        f"Block: {block_number} -- Returned {len(classified_traces)} classified traces"
    )

    if should_write_classified_traces:
        delete_classified_traces_for_block(inspect_db_session, block_number)
        write_classified_traces(inspect_db_session, classified_traces)

    transfers = get_transfers(classified_traces)
    logger.info(f"Block: {block_number} -- Found {len(transfers)} transfers")

    delete_transfers_for_block(inspect_db_session, block_number)
    write_transfers(inspect_db_session, transfers)

    swaps = get_swaps(classified_traces)
    logger.info(f"Block: {block_number} -- Found {len(swaps)} swaps")

    delete_swaps_for_block(inspect_db_session, block_number)
    write_swaps(inspect_db_session, swaps)

    arbitrages = get_arbitrages(swaps)
    logger.info(f"Block: {block_number} -- Found {len(arbitrages)} arbitrages")

    delete_arbitrages_for_block(inspect_db_session, block_number)
    write_arbitrages(inspect_db_session, arbitrages)

    liquidations = get_liquidations(classified_traces)
    logger.info(f"Block: {block_number} -- Found {len(liquidations)} liquidations")

    delete_liquidations_for_block(inspect_db_session, block_number)
    write_liquidations(inspect_db_session, liquidations)

    punk_bids = get_punk_bids(classified_traces)
    punk_bid_acceptances = get_punk_bid_acceptances(classified_traces)

    punk_snipes = get_punk_snipes(punk_bids, punk_bid_acceptances)
    logger.info(f"Block: {block_number} -- Found {len(punk_snipes)} punk snipes")

    miner_payments = get_miner_payments(
        block.miner, block.base_fee_per_gas, classified_traces, block.receipts
    )

    delete_miner_payments_for_block(inspect_db_session, block_number)
    write_miner_payments(inspect_db_session, miner_payments)
