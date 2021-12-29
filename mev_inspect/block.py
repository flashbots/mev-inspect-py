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
    base_provider,
    w3: Web3,
    block_number: int,
    trace_db_session: Optional[orm.Session],
) -> Block:
    block: Optional[Block] = None

    if trace_db_session is not None:
        block = _find_block(trace_db_session, block_number)

    if block is None:
        block = await _fetch_block(w3, base_provider, block_number)
        return block
    else:
        return block


async def _fetch_block(w3, base_provider, block_number: int, retries: int = 0) -> Block:
    block_json, receipts_json, traces_json, base_fee_per_gas = await asyncio.gather(
        w3.eth.get_block(block_number),
        base_provider.make_request("eth_getBlockReceipts", [block_number]),
        base_provider.make_request("trace_block", [block_number]),
        fetch_base_fee_per_gas(w3, block_number),
    )

    try:
        receipts: List[Receipt] = [
            Receipt(**receipt) for receipt in receipts_json["result"]
        ]
        traces = [Trace(**trace_json) for trace_json in traces_json["result"]]
    except KeyError as e:
        logger.warning(
            f"Failed to create objects from block: {block_number}: {e}, retrying: {retries + 1} / 3"
        )
        if retries < 3:
            await asyncio.sleep(5)
            return await _fetch_block(w3, base_provider, block_number, retries)
        else:
            raise

    return Block(
        block_number=block_number,
        block_timestamp=block_json["timestamp"],
        miner=block_json["miner"],
        base_fee_per_gas=base_fee_per_gas,
        traces=traces,
        receipts=receipts,
    )


def _find_block(
    trace_db_session: orm.Session,
    block_number: int,
) -> Optional[Block]:
    block_timestamp = _find_block_timestamp(trace_db_session, block_number)
    if block_timestamp is None:
        return None

    base_fee_per_gas = _find_base_fee(trace_db_session, block_number)
    if base_fee_per_gas is None:
        return None

    traces = _find_traces(trace_db_session, block_number)
    if traces is None:
        return None

    receipts = _find_receipts(trace_db_session, block_number)
    if receipts is None:
        return None

    miner_address = _get_miner_address_from_traces(traces)
    if miner_address is None:
        return None

    return Block(
        block_number=block_number,
        block_timestamp=block_timestamp,
        miner=miner_address,
        base_fee_per_gas=base_fee_per_gas,
        traces=traces,
        receipts=receipts,
    )


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


def _find_traces(
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


def _find_receipts(
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


def _find_base_fee(
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
