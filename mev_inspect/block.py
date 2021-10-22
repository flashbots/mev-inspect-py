import asyncio
from pathlib import Path
from typing import List, Optional

from sqlalchemy import orm
from web3 import Web3

from mev_inspect.fees import fetch_base_fee_per_gas
from mev_inspect.schemas import Block, Trace, TraceType
from mev_inspect.schemas.receipts import Receipt


cache_directory = "./cache"


def get_latest_block_number(w3: Web3) -> int:
    return int(w3.eth.get_block("latest")["number"])


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


async def _fetch_block(
    w3,
    base_provider,
    block_number: int,
) -> Block:
    block_json, receipts_json, traces_json, base_fee_per_gas = await asyncio.gather(
        w3.eth.get_block(block_number),
        base_provider.make_request("eth_getBlockReceipts", [block_number]),
        base_provider.make_request("trace_block", [block_number]),
        fetch_base_fee_per_gas(w3, block_number),
    )

    receipts: List[Receipt] = [
        Receipt(**receipt) for receipt in receipts_json["result"]
    ]
    traces = [Trace(**trace_json) for trace_json in traces_json["result"]]

    return Block(
        block_number=block_number,
        miner=block_json["miner"],
        base_fee_per_gas=base_fee_per_gas,
        traces=traces,
        receipts=receipts,
    )


def _find_block(
    trace_db_session: orm.Session,
    block_number: int,
) -> Optional[Block]:
    traces = _find_traces(trace_db_session, block_number)
    receipts = _find_receipts(trace_db_session, block_number)
    base_fee_per_gas = _find_base_fee(trace_db_session, block_number)

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


def cache_block(cache_path: Path, block: Block):
    write_mode = "w" if cache_path.is_file() else "x"

    cache_path.parent.mkdir(parents=True, exist_ok=True)

    with open(cache_path, mode=write_mode) as cache_file:
        cache_file.write(block.json())


def _get_cache_path(block_number: int) -> Path:
    cache_directory_path = Path(cache_directory)
    return cache_directory_path / f"{block_number}.json"
