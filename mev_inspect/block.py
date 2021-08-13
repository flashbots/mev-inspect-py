from pathlib import Path
from typing import Any, Dict, List

from web3 import Web3

from mev_inspect.schemas import Block, Trace, TraceType


cache_directory = "./cache"


## Creates a block object, either from the cache or from the chain itself
## Note that you need to pass in the provider, not the web3 wrapped provider object!
## This is because only the provider allows you to make json rpc requests
def create_from_block_number(block_number: int, base_provider) -> Block:
    cache_path = _get_cache_path(block_number)

    if cache_path.is_file():
        print(f"Cache for block {block_number} exists, " "loading data from cache")

        return Block.parse_file(cache_path)
    else:
        print(f"Cache for block {block_number} did not exist, getting data")

        w3 = Web3(base_provider)
        block = fetch_block(w3, base_provider, block_number)

        cache_block(cache_path, block)

        return block


def fetch_block(w3, base_provider, block_number: int) -> Block:
    ## Get block data
    block_data = w3.eth.get_block(block_number, True)

    ## Get the block receipts
    ## TODO: evaluate whether or not this is sufficient or if gas used needs to be converted to a proper big number.
    ## In inspect-ts it needed to be converted
    block_receipts_raw = base_provider.make_request(
        "eth_getBlockReceipts", [block_number]
    )

    ## Trace the whole block, return those calls
    traces_json = w3.parity.trace_block(block_number)
    traces = [Trace(**trace_json) for trace_json in traces_json]

    ## Get the logs
    block_hash = (block_data.hash).hex()
    block_logs = w3.eth.get_logs({"blockHash": block_hash})

    ## Get gas used by individual txs and store them too
    txs_gas_data: Dict[str, Dict[str, Any]] = {}
    """
    for transaction in block_data["transactions"]:
        tx_hash = (transaction.hash).hex()
        tx_data = w3.eth.get_transaction(tx_hash)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        txs_gas_data[tx_hash] = {
            "gasUsed": tx_receipt[
                "gasUsed"
            ],  # fix: why does this return 0 for certain txs?
            "gasPrice": tx_data["gasPrice"],
            "netFeePaid": tx_data["gasPrice"] * tx_receipt["gasUsed"],
        }
    """
    transaction_hashes = get_transaction_hashes(traces)

    ## Create a new object
    return Block(
        block_number=block_number,
        data=block_data,
        receipts=block_receipts_raw,
        traces=traces,
        logs=block_logs,
        transaction_hashes=transaction_hashes,
        txs_gas_data=txs_gas_data,
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

    with open(cache_path, mode=write_mode) as cache_file:
        cache_file.write(block.json())


def _get_cache_path(block_number: int) -> Path:
    cache_directory_path = Path(cache_directory)
    return cache_directory_path / f"{block_number}-new.json"
