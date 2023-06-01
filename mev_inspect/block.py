import asyncio
import logging
from typing import List, Optional

from sqlalchemy import orm
from web3 import Web3

from mev_inspect.fees import fetch_base_fee_per_gas
from mev_inspect.schemas.blocks import Block
from mev_inspect.schemas.receipts import Receipt
from mev_inspect.schemas.traces import Trace, TraceType
from mev_inspect.utils import hex_to_int

logger = logging.getLogger(__name__)


async def get_latest_block_number(base_provider) -> int:
    latest_block = await base_provider.make_request(
        "eth_getBlockByNumber",
        ["latest", False],
    )

    return hex_to_int(latest_block["result"]["number"])


async def create_from_block_number(
    w3: Web3,
    block_number: int,
    trace_db_session: Optional[orm.Session],
) -> Block:
    block_timestamp, receipts, traces, base_fee_per_gas = await asyncio.gather(
        _find_or_fetch_block_timestamp(w3, block_number, trace_db_session),
        _find_or_fetch_block_receipts(w3, block_number, trace_db_session),
        _find_or_fetch_block_traces(w3, block_number, trace_db_session),
        _find_or_fetch_base_fee_per_gas(w3, block_number, trace_db_session),
    )

    # filter out failed transactions
    failed_transactions = set(
        receipt.transaction_hash for receipt in receipts if receipt.status == 0
    )
    receipts = [
        receipt
        for receipt in receipts
        if receipt.transaction_hash not in failed_transactions
    ]
    traces = [
        trace for trace in traces if trace.transaction_hash not in failed_transactions
    ]

    miner_address = _get_miner_address_from_traces(traces)

    return Block(
        block_number=block_number,
        block_timestamp=block_timestamp,
        miner=miner_address,
        base_fee_per_gas=base_fee_per_gas,
        traces=traces,
        receipts=receipts,
    )


async def _find_or_fetch_block_timestamp(
    w3,
    block_number: int,
    trace_db_session: Optional[orm.Session],
) -> int:
    if trace_db_session is not None:
        existing_block_timestamp = _find_block_timestamp(trace_db_session, block_number)
        if existing_block_timestamp is not None:
            return existing_block_timestamp

    return await _fetch_block_timestamp(w3, block_number)


async def _find_or_fetch_block_receipts(
    w3,
    block_number: int,
    trace_db_session: Optional[orm.Session],
) -> List[Receipt]:
    if trace_db_session is not None:
        existing_block_receipts = _find_block_receipts(trace_db_session, block_number)
        if existing_block_receipts is not None:
            return existing_block_receipts

    return await _fetch_block_receipts(w3, block_number)


async def _find_or_fetch_block_traces(
    w3,
    block_number: int,
    trace_db_session: Optional[orm.Session],
) -> List[Trace]:
    if trace_db_session is not None:
        existing_block_traces = _find_block_traces(trace_db_session, block_number)
        if existing_block_traces is not None:
            return existing_block_traces

    return await _fetch_block_traces(w3, block_number)


async def _find_or_fetch_base_fee_per_gas(
    w3,
    block_number: int,
    trace_db_session: Optional[orm.Session],
) -> int:
    if trace_db_session is not None:
        existing_base_fee_per_gas = _find_base_fee_per_gas(
            trace_db_session, block_number
        )
        if existing_base_fee_per_gas is not None:
            return existing_base_fee_per_gas

    return await fetch_base_fee_per_gas(w3, block_number)


async def _fetch_block_timestamp(w3, block_number: int) -> int:
    block_json = await w3.eth.get_block(block_number)
    return block_json["timestamp"]


async def _fetch_block_receipts(w3, block_number: int) -> List[Receipt]:
    receipts_json = await w3.eth.get_block_receipts(block_number)
    return [Receipt(**receipt) for receipt in receipts_json]


async def _fetch_block_traces(w3, block_number: int) -> List[Trace]:
    traces_json = await w3.eth.trace_block(block_number)
    return [Trace(**trace_json) for trace_json in traces_json]


def _find_block_timestamp(
    trace_db_session: orm.Session,
    block_number: int,
) -> Optional[int]:
    result = trace_db_session.execute(
        "SELECT block_timestamp FROM block_timestamps WHERE block_number = :block_number",
        params={"block_number": block_number},
    ).one_or_none()

    if result is None:
        return None
    else:
        (block_timestamp,) = result
        return block_timestamp


def _find_block_traces(
    trace_db_session: orm.Session,
    block_number: int,
) -> Optional[List[Trace]]:
    result = trace_db_session.execute(
        "SELECT raw_traces FROM block_traces WHERE block_number = :block_number",
        params={"block_number": block_number},
    ).one_or_none()

    if result is None:
        return None
    else:
        (traces_json,) = result
        return [Trace(**trace_json) for trace_json in traces_json]


def _find_block_receipts(
    trace_db_session: orm.Session,
    block_number: int,
) -> Optional[List[Receipt]]:
    result = trace_db_session.execute(
        "SELECT raw_receipts FROM block_receipts WHERE block_number = :block_number",
        params={"block_number": block_number},
    ).one_or_none()

    if result is None:
        return None
    else:
        (receipts_json,) = result
        return [Receipt(**receipt) for receipt in receipts_json]


def _find_base_fee_per_gas(
    trace_db_session: orm.Session,
    block_number: int,
) -> Optional[int]:
    result = trace_db_session.execute(
        "SELECT base_fee_in_wei FROM base_fee WHERE block_number = :block_number",
        params={"block_number": block_number},
    ).one_or_none()

    if result is None:
        return None
    else:
        (base_fee,) = result
        return base_fee


def _get_miner_address_from_traces(traces: List[Trace]) -> Optional[str]:
    for trace in traces:
        if trace.type == TraceType.reward:
            return trace.action["author"]

    return None


def get_transaction_hashes(calls: List[Trace]) -> List[str]:
    result = []

    for call in calls:
        if call.type != TraceType.reward:
            if (
                call.transaction_hash is not None
                and call.transaction_hash not in result
            ):
                result.append(call.transaction_hash)

    return result
