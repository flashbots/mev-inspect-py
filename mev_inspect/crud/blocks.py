from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from mev_inspect.schemas.blocks import Block
from mev_inspect.schemas.receipts import Receipt
from mev_inspect.schemas.traces import Trace, TraceType


async def find_block(
    trace_db_session: AsyncSession,
    block_number: int,
) -> Optional[Block]:
    traces = await _find_traces(trace_db_session, block_number)
    receipts = await _find_receipts(trace_db_session, block_number)
    base_fee_per_gas = await _find_base_fee(trace_db_session, block_number)

    if traces is None or receipts is None or base_fee_per_gas is None:
        return None

    miner_address = _get_miner_address_from_traces(traces)

    if miner_address is None:
        return None

    return Block(
        block_number=block_number,
        miner=miner_address,
        base_fee_per_gas=base_fee_per_gas,
        traces=traces,
        receipts=receipts,
    )


async def _find_traces(
    trace_db_session: AsyncSession,
    block_number: int,
) -> Optional[List[Trace]]:
    result = await trace_db_session.execute(
        "SELECT raw_traces FROM block_traces WHERE block_number = :block_number",
        params={"block_number": block_number},
    ).one_or_none()

    if result is None:
        return None
    else:
        (traces_json,) = result
        return [Trace(**trace_json) for trace_json in traces_json]


async def _find_receipts(
    trace_db_session: AsyncSession,
    block_number: int,
) -> Optional[List[Receipt]]:
    result = await trace_db_session.execute(
        "SELECT raw_receipts FROM block_receipts WHERE block_number = :block_number",
        params={"block_number": block_number},
    ).one_or_none()

    if result is None:
        return None
    else:
        (receipts_json,) = result
        return [Receipt(**receipt) for receipt in receipts_json]


async def _find_base_fee(
    trace_db_session: AsyncSession,
    block_number: int,
) -> Optional[int]:
    result = await trace_db_session.execute(
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
