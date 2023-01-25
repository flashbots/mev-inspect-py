import asyncio
import logging
from time import sleep
from typing import Dict, List, Optional, Tuple

from sqlalchemy import orm
from web3 import Web3

from mev_inspect.fees import fetch_base_fee_per_gas
from mev_inspect.schemas.blocks import Block
from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.receipts import Receipt
from mev_inspect.schemas.swaps import Swap
from mev_inspect.schemas.traces import Trace, TraceType
from mev_inspect.utils import hex_to_int

logger = logging.getLogger(__name__)

TOPIC_SWAP = "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822"
TOPIC_LIQUIDATION = "0xe413a321e8681d831f4dbccbca790d2952b56f977908e45be37335533e005286"
UNI_TOKEN_0 = "0x0dfe1681"
UNI_TOKEN_1 = "0xd21220a7"


async def _get_logs_for_topics(base_provider, after_block, before_block, topics):
    while True:
        try:
            logs = await base_provider.make_request(
                "eth_getLogs",
                [
                    {
                        "fromBlock": hex(after_block),
                        "toBlock": hex(before_block),
                        "topics": topics,
                    }
                ],
            )

            return logs["result"]
        except Exception as e:
            print(f"Error, retrying {e}")
            sleep(0.05)


def _logs_by_tx(logs):
    logs_by_tx = dict()
    for log in logs:
        transaction_hash = log["transactionHash"]
        if transaction_hash in logs_by_tx.keys():
            logs_by_tx[transaction_hash].append(log)
        else:
            logs_by_tx[transaction_hash] = [log]
    return logs_by_tx


def get_swap(data):
    data = data[2:]
    return (
        int(data[0:64], base=16),
        int(data[64:128], base=16),
        int(data[128:192], base=16),
        int(data[192:256], base=16),
    )


def get_liquidation(data):
    data = data[2:]
    return (
        int(data[0:64], base=16),
        int(data[64:128], base=16),
        "0x" + data[128 + 24 : 168 + 24],
    )


async def classify_logs(logs, pool_reserves, w3):
    cswaps = []
    cliquidations = []

    for log in logs:
        topic = log["topics"][0]
        if topic in [TOPIC_SWAP, TOPIC_LIQUIDATION]:
            block = int(log["blockNumber"], 16)
            transaction_hash = log["transactionHash"]
            trace_address = [int(log["logIndex"], 16)]
            first_token = "0x" + log["topics"][1][26:]
            second_token = "0x" + log["topics"][2][26:]
        if topic == TOPIC_SWAP:
            pool_address = log["address"]
            if pool_address in pool_reserves:
                token0, token1 = pool_reserves[pool_address]
            else:
                addr = Web3.toChecksumAddress(pool_address)
                while True:
                    try:
                        token0, token1 = await asyncio.gather(
                            w3.eth.call({"to": addr, "data": UNI_TOKEN_0}),
                            w3.eth.call({"to": addr, "data": UNI_TOKEN_1}),
                        )
                        token0 = w3.toHex(token0)
                        token1 = w3.toHex(token1)
                        pool_reserves[pool_address] = (token0, token1)
                        break
                    except Exception as e:
                        print(f"Error, retrying {e}")
                        sleep(0.05)

            am0in, am1in, am0out, am1out = get_swap(log["data"])
            swap = Swap(
                abi_name="uniswap_v2",
                transaction_hash=transaction_hash,
                block_number=block,
                trace_address=trace_address,
                contract_address=pool_address,
                from_address=first_token,
                to_address=second_token,
                token_in_address=token0 if am0in != 0 else token1,
                token_in_amount=am0in if am0in != 0 else am1in,
                token_out_address=token1 if am1out != 0 else token0,
                token_out_amount=am0out if am0out != 0 else am1out,
                protocol=None,
                error=None,
            )
            cswaps.append(swap)
        elif topic == TOPIC_LIQUIDATION:
            block = str(block)
            am_debt, am_recv, addr_usr = get_liquidation(log["data"])
            liquidation = Liquidation(
                liquidated_user="0x" + log["topics"][3][26:],
                liquidator_user=addr_usr,
                debt_token_address=second_token,
                debt_purchase_amount=am_debt,
                received_amount=am_recv,
                received_token_address=first_token,
                protocol=None,
                transaction_hash=transaction_hash,
                trace_address=trace_address,
                block_number=block,
                error=None,
            )
            cliquidations.append(liquidation)

    return cswaps, cliquidations


reserves: Dict[str, Tuple[str, str]] = dict()


async def get_classified_traces_from_events(
    w3: Web3, after_block: int, before_block: int
):
    base_provider = w3.provider
    start = after_block
    stride = 300
    while start < before_block:
        begin = start
        end = start + stride if (start + stride) < before_block else before_block - 1
        start += stride
        print("fetching from node...", begin, end, flush=True)
        all_logs = await _get_logs_for_topics(
            base_provider, begin, end, [[TOPIC_SWAP, TOPIC_LIQUIDATION]]
        )
        logs_by_tx = _logs_by_tx(all_logs)
        for tx in logs_by_tx.keys():
            yield await classify_logs(logs_by_tx[tx], reserves, w3)


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
