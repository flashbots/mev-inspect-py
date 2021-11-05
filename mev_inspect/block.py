import asyncio
import logging
import sys
from pathlib import Path
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from web3 import Web3

from mev_inspect.crud.blocks import find_block
from mev_inspect.fees import fetch_base_fee_per_gas
from mev_inspect.schemas.blocks import Block
from mev_inspect.schemas.receipts import Receipt
from mev_inspect.schemas.traces import Trace, TraceType


cache_directory = "./cache"
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


def get_latest_block_number(w3: Web3) -> int:
    return int(w3.eth.get_block("latest")["number"])


async def create_from_block_number(
    base_provider,
    w3: Web3,
    block_number: int,
    trace_db_session: Optional[AsyncSession],
) -> Block:
    block: Optional[Block] = None

    if trace_db_session is not None:
        block = await find_block(trace_db_session, block_number)

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
        miner=block_json["miner"],
        base_fee_per_gas=base_fee_per_gas,
        traces=traces,
        receipts=receipts,
    )


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
