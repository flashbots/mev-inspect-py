import asyncio
import logging
from typing import List, Optional
import json
import aiohttp

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
    geth: bool,
    block_number: int,
    trace_db_session: Optional[orm.Session],
) -> Block:
    block: Optional[Block] = None

    if trace_db_session is not None:
        block = _find_block(trace_db_session, block_number)

    if block is None:
        block = await _fetch_block(w3, base_provider, geth, block_number)
        return block
    return block


async def _fetch_block(
    w3, base_provider, geth: bool, block_number: int, retries: int = 0
) -> Block:
    if not geth:
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
            return Block(
                block_number=block_number,
                block_timestamp=block_json["timestamp"],
                miner=block_json["miner"],
                base_fee_per_gas=base_fee_per_gas,
                traces=traces,
                receipts=receipts,
            )
        except KeyError as e:
            logger.warning(
                f"Failed to create objects from block: {block_number}: {e}, retrying: {retries + 1} / 3"
            )
            if retries < 3:
                await asyncio.sleep(5)
                return await _fetch_block(
                    w3, base_provider, geth, block_number, retries
                )
            else:
                raise
    else:
        # print(block_number)
        block_json = await asyncio.gather(w3.eth.get_block(block_number))
        traces = await geth_get_tx_traces_parity_format(base_provider, block_json[0])
        geth_tx_receipts = await geth_get_tx_receipts_async(
            base_provider.endpoint_uri, block_json[0]["transactions"]
        )
        receipts = geth_receipts_translator(block_json[0], geth_tx_receipts)
        base_fee_per_gas = 0

        return Block(
            block_number=block_number,
            block_timestamp=block_json[0]["timestamp"],
            miner=block_json[0]["miner"],
            base_fee_per_gas=base_fee_per_gas,
            traces=traces,
            receipts=receipts,
        )


def _find_block(
    trace_db_session: orm.Session,
    block_number: int,
) -> Optional[Block]:
    block_timestamp = _find_block_timestamp(trace_db_session, block_number)
    traces = _find_traces(trace_db_session, block_number)
    receipts = _find_receipts(trace_db_session, block_number)
    base_fee_per_gas = _find_base_fee(trace_db_session, block_number)

    if (
        block_timestamp is None
        or traces is None
        or receipts is None
        or base_fee_per_gas is None
    ):
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


# Geth specific additions


async def geth_get_tx_traces_parity_format(base_provider, block_json: dict):
    # print(block_json['hash'].hex())
    block_hash = block_json["hash"]
    block_trace = await geth_get_tx_traces(base_provider, block_hash)
    # print(block_trace)
    parity_traces = []
    for idx, trace in enumerate(block_trace["result"]):
        if "result" in trace:
            parity_traces.extend(
                unwrap_tx_trace_for_parity(block_json, idx, trace["result"])
            )
    return parity_traces


async def geth_get_tx_traces(base_provider, block_hash):
    block_trace = await base_provider.make_request(
        "debug_traceBlockByHash", [block_hash.hex(), {"tracer": "callTracer"}]
    )
    return block_trace


def unwrap_tx_trace_for_parity(
    block_json, tx_pos_in_block, tx_trace, position=[]
) -> List[Trace]:
    response_list = []
    _calltype_mapping = {
        "CALL": "call",
        "DELEGATECALL": "delegateCall",
        "CREATE": "create",
        "SUICIDE": "suicide",
        "REWARD": "reward",
    }
    try:
        if tx_trace["type"] == "STATICCALL":
            return []
        action_dict = dict()
        action_dict["callType"] = _calltype_mapping[tx_trace["type"]]
        if action_dict["callType"] == "call":
            action_dict["value"] = tx_trace["value"]
        for key in ["from", "to", "gas", "input"]:
            action_dict[key] = tx_trace[key]

        result_dict = dict()
        for key in ["gasUsed", "output"]:
            result_dict[key] = tx_trace[key]

        response_list.append(
            Trace(
                action=action_dict,
                block_hash=str(block_json["hash"]),
                block_number=int(block_json["number"]),
                result=result_dict,
                subtraces=len(tx_trace["calls"]) if "calls" in tx_trace.keys() else 0,
                trace_address=position,
                transaction_hash=block_json["transactions"][tx_pos_in_block].hex(),
                transaction_position=tx_pos_in_block,
                type=TraceType(_calltype_mapping[tx_trace["type"]]),
            )
        )
    except Exception:
        return []

    if "calls" in tx_trace.keys():
        for idx, subcall in enumerate(tx_trace["calls"]):
            response_list.extend(
                unwrap_tx_trace_for_parity(
                    block_json, tx_pos_in_block, subcall, position + [idx]
                )
            )
    return response_list


async def geth_get_tx_receipts_task(session, endpoint_uri, tx):
    data = {
        "jsonrpc": "2.0",
        "id": "0",
        "method": "eth_getTransactionReceipt",
        "params": [tx.hex()],
    }
    async with session.post(endpoint_uri, json=data) as response:
        if response.status != 200:
            response.raise_for_status()
        return await response.text()


async def geth_get_tx_receipts_async(endpoint_uri, transactions):
    geth_tx_receipts = []
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(geth_get_tx_receipts_task(session, endpoint_uri, tx))
            for tx in transactions
        ]
        geth_tx_receipts = await asyncio.gather(*tasks)
    return [json.loads(tx_receipts) for tx_receipts in geth_tx_receipts]


def geth_receipts_translator(block_json, geth_tx_receipts) -> List[Receipt]:
    json_decoded_receipts = [
        tx_receipt["result"]
        if tx_receipt != None and ("result" in tx_receipt.keys())
        else None
        for tx_receipt in geth_tx_receipts
    ]
    results = []
    for idx, tx_receipt in enumerate(json_decoded_receipts):
        if tx_receipt != None:
            results.append(unwrap_tx_receipt_for_parity(block_json, idx, tx_receipt))
    return results


def unwrap_tx_receipt_for_parity(block_json, tx_pos_in_block, tx_receipt) -> Receipt:
    try:
        if tx_pos_in_block != int(tx_receipt["transactionIndex"], 16):
            print(
                "Alert the position of transaction in block is mismatched ",
                tx_pos_in_block,
                tx_receipt["transactionIndex"],
            )
        return Receipt(
            block_number=block_json["number"],
            transaction_hash=tx_receipt["transactionHash"],
            transaction_index=tx_pos_in_block,
            gas_used=tx_receipt["gasUsed"],
            effective_gas_price=tx_receipt["effectiveGasPrice"],
            cumulative_gas_used=tx_receipt["cumulativeGasUsed"],
            to=tx_receipt["to"],
        )

    except Exception as e:
        print("error while decoding receipt", tx_receipt, e)

    return Receipt()
