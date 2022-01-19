import logging
from typing import List, Optional

from sqlalchemy import orm
from web3 import Web3

from mev_inspect.arbitrages import get_arbitrages
from mev_inspect.block import create_from_block_number
from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.crud.arbitrages import delete_arbitrages_for_blocks, write_arbitrages
from mev_inspect.crud.blocks import delete_blocks, write_blocks
from mev_inspect.crud.liquidations import (
    delete_liquidations_for_blocks,
    write_liquidations,
)
from mev_inspect.crud.miner_payments import (
    delete_miner_payments_for_blocks,
    write_miner_payments,
)
from mev_inspect.crud.nft_trades import delete_nft_trades_for_blocks, write_nft_trades
from mev_inspect.crud.punks import (
    delete_punk_bid_acceptances_for_blocks,
    delete_punk_bids_for_blocks,
    delete_punk_snipes_for_blocks,
    write_punk_bid_acceptances,
    write_punk_bids,
    write_punk_snipes,
)
from mev_inspect.crud.sandwiches import delete_sandwiches_for_blocks, write_sandwiches
from mev_inspect.crud.summary import update_summary_for_block_range
from mev_inspect.crud.swaps import delete_swaps_for_blocks, write_swaps
from mev_inspect.crud.traces import (
    delete_classified_traces_for_blocks,
    write_classified_traces,
)
from mev_inspect.crud.transfers import delete_transfers_for_blocks, write_transfers
from mev_inspect.liquidations import get_liquidations
from mev_inspect.miner_payments import get_miner_payments
from mev_inspect.nft_trades import get_nft_trades
from mev_inspect.punks import get_punk_bid_acceptances, get_punk_bids, get_punk_snipes
from mev_inspect.sandwiches import get_sandwiches
from mev_inspect.schemas.arbitrages import Arbitrage
from mev_inspect.schemas.blocks import Block
from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.miner_payments import MinerPayment
from mev_inspect.schemas.nft_trades import NftTrade
from mev_inspect.schemas.punk_accept_bid import PunkBidAcceptance
from mev_inspect.schemas.punk_bid import PunkBid
from mev_inspect.schemas.punk_snipe import PunkSnipe
from mev_inspect.schemas.sandwiches import Sandwich
from mev_inspect.schemas.swaps import Swap
from mev_inspect.schemas.traces import ClassifiedTrace
from mev_inspect.schemas.transfers import Transfer
from mev_inspect.swaps import get_swaps
from mev_inspect.transfers import get_transfers

logger = logging.getLogger(__name__)


async def inspect_block(
    inspect_db_session: orm.Session,
    w3: Web3,
    trace_classifier: TraceClassifier,
    block_number: int,
    trace_db_session: Optional[orm.Session],
    should_write_classified_traces: bool = True,
):
    await inspect_many_blocks(
        inspect_db_session,
        w3,
        trace_classifier,
        block_number,
        block_number + 1,
        trace_db_session,
        should_write_classified_traces,
    )


async def inspect_many_blocks(
    inspect_db_session: orm.Session,
    w3: Web3,
    trace_classifier: TraceClassifier,
    after_block_number: int,
    before_block_number: int,
    trace_db_session: Optional[orm.Session],
    should_write_classified_traces: bool = True,
):
    all_blocks: List[Block] = []
    all_classified_traces: List[ClassifiedTrace] = []
    all_transfers: List[Transfer] = []
    all_swaps: List[Swap] = []
    all_arbitrages: List[Arbitrage] = []
    all_liquidations: List[Liquidation] = []
    all_sandwiches: List[Sandwich] = []

    all_punk_bids: List[PunkBid] = []
    all_punk_bid_acceptances: List[PunkBidAcceptance] = []
    all_punk_snipes: List[PunkSnipe] = []

    all_miner_payments: List[MinerPayment] = []

    all_nft_trades: List[NftTrade] = []

    for block_number in range(after_block_number, before_block_number):
        block = await create_from_block_number(
            w3,
            block_number,
            trace_db_session,
        )

        logger.info(f"Block: {block_number} -- Total traces: {len(block.traces)}")

        total_transactions = len(
            set(
                t.transaction_hash
                for t in block.traces
                if t.transaction_hash is not None
            )
        )
        logger.info(
            f"Block: {block_number} -- Total transactions: {total_transactions}"
        )

        classified_traces = trace_classifier.classify(block.traces)
        logger.info(
            f"Block: {block_number} -- Returned {len(classified_traces)} classified traces"
        )

        transfers = get_transfers(classified_traces)
        logger.info(f"Block: {block_number} -- Found {len(transfers)} transfers")

        swaps = get_swaps(classified_traces)
        logger.info(f"Block: {block_number} -- Found {len(swaps)} swaps")

        arbitrages = get_arbitrages(swaps)
        logger.info(f"Block: {block_number} -- Found {len(arbitrages)} arbitrages")

        liquidations = get_liquidations(classified_traces)
        logger.info(f"Block: {block_number} -- Found {len(liquidations)} liquidations")

        sandwiches = get_sandwiches(swaps)
        logger.info(f"Block: {block_number} -- Found {len(sandwiches)} sandwiches")

        punk_bids = get_punk_bids(classified_traces)
        punk_bid_acceptances = get_punk_bid_acceptances(classified_traces)
        punk_snipes = get_punk_snipes(punk_bids, punk_bid_acceptances)
        logger.info(f"Block: {block_number} -- Found {len(punk_snipes)} punk snipes")

        nft_trades = get_nft_trades(classified_traces)
        logger.info(f"Block: {block_number} -- Found {len(nft_trades)} nft trades")

        miner_payments = get_miner_payments(
            block.miner, block.base_fee_per_gas, classified_traces, block.receipts
        )

        all_blocks.append(block)
        all_classified_traces.extend(classified_traces)
        all_transfers.extend(transfers)
        all_swaps.extend(swaps)
        all_arbitrages.extend(arbitrages)
        all_liquidations.extend(liquidations)
        all_sandwiches.extend(sandwiches)

        all_punk_bids.extend(punk_bids)
        all_punk_bid_acceptances.extend(punk_bid_acceptances)
        all_punk_snipes.extend(punk_snipes)

        all_nft_trades.extend(nft_trades)

        all_miner_payments.extend(miner_payments)

    logger.info("Writing data")
    delete_blocks(inspect_db_session, after_block_number, before_block_number)
    write_blocks(inspect_db_session, all_blocks)

    if should_write_classified_traces:
        delete_classified_traces_for_blocks(
            inspect_db_session, after_block_number, before_block_number
        )
        write_classified_traces(inspect_db_session, all_classified_traces)

    delete_transfers_for_blocks(
        inspect_db_session, after_block_number, before_block_number
    )
    write_transfers(inspect_db_session, all_transfers)

    delete_swaps_for_blocks(inspect_db_session, after_block_number, before_block_number)
    write_swaps(inspect_db_session, all_swaps)

    delete_arbitrages_for_blocks(
        inspect_db_session, after_block_number, before_block_number
    )
    write_arbitrages(inspect_db_session, all_arbitrages)

    delete_liquidations_for_blocks(
        inspect_db_session, after_block_number, before_block_number
    )
    write_liquidations(inspect_db_session, all_liquidations)

    delete_sandwiches_for_blocks(
        inspect_db_session, after_block_number, before_block_number
    )
    write_sandwiches(inspect_db_session, all_sandwiches)

    delete_punk_bids_for_blocks(
        inspect_db_session, after_block_number, before_block_number
    )
    write_punk_bids(inspect_db_session, all_punk_bids)

    delete_punk_bid_acceptances_for_blocks(
        inspect_db_session, after_block_number, before_block_number
    )
    write_punk_bid_acceptances(inspect_db_session, all_punk_bid_acceptances)

    delete_punk_snipes_for_blocks(
        inspect_db_session, after_block_number, before_block_number
    )
    write_punk_snipes(inspect_db_session, all_punk_snipes)

    delete_nft_trades_for_blocks(
        inspect_db_session, after_block_number, before_block_number
    )
    write_nft_trades(inspect_db_session, all_nft_trades)

    delete_miner_payments_for_blocks(
        inspect_db_session, after_block_number, before_block_number
    )
    write_miner_payments(inspect_db_session, all_miner_payments)

    update_summary_for_block_range(
        inspect_db_session,
        after_block_number,
        before_block_number,
    )

    logger.info("Done writing")
