import json
from pathlib import Path
from typing import List

from web3 import Web3

from schemas import Block


cache_directory = './cache'


def get_transaction_hashes(calls: List[dict]) -> List[str]:
    result = []

    for call in calls:
        if call['type'] != 'reward':
            if call['transactionHash'] in result:
                continue
            else:
                result.append(call['transactionHash'])
    
    return result


def write_json(block: Block):
    cache_path = _get_cache_path(block.block_number)
    write_mode = "w" if cache_path.is_file() else "x"

    with open(cache_path, mode=write_mode) as cache_file:
        cache_file.write(block.json(sort_keys=True, indent=4))


## Creates a block object, either from the cache or from the chain itself
## Note that you need to pass in the provider, not the web3 wrapped provider object!
## This is because only the provider allows you to make json rpc requests
def createFromBlockNumber(block_number: int, base_provider) -> Block:
    cache_path = _get_cache_path(block_number)
    
    ## Check to see if the data already exists in the cache
    ## if it exists load the data from cache
    ## If not then get the data from the chain and save it to the cache
    if (cache_path.is_file()):
        print(
            f'Cache for block {block_number} exists, ' \
            'loading data from cache'
        )

        block = Block.parse_file(cache_path)
        return block
    else:
        w3 = Web3(base_provider)
        print(("Cache for block {block_number} did not exist, getting data").format(block_number=block_number))
        
        ## Get block data
        block_data = w3.eth.get_block(block_number, True)
        
        ## Get the block receipts
        ## TODO: evaluate whether or not this is sufficient or if gas used needs to be converted to a proper big number.
        ## In inspect-ts it needed to be converted
        block_receipts_raw = base_provider.make_request("eth_getBlockReceipts", [block_number])

        ## Trace the whole block, return those calls
        block_calls = w3.parity.trace_block(block_number)
        
        ## Get the logs
        block_hash = (block_data.hash).hex()
        block_logs = w3.eth.get_logs({'blockHash': block_hash})

        ## Get gas used by individual txs and store them too
        txs_gas_data = {}
        for transaction in block_data['transactions']:
            tx_hash = (transaction.hash).hex()
            tx_data = w3.eth.get_transaction(tx_hash)
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            txs_gas_data[tx_hash] = {
                'gasUsed': tx_receipt['gasUsed'], # fix: why does this return 0 for certain txs?
                'gasPrice': tx_data['gasPrice'],
                'netFeePaid': tx_data['gasPrice'] * tx_receipt['gasUsed']
            }
        
        transaction_hashes = get_transaction_hashes(block_calls)

        ## Create a new object
        block = Block(
            block_number=block_number,
            data=block_data,
            receipts=block_receipts_raw,
            calls=block_calls,
            logs=block_logs,
            transaction_hashes=transaction_hashes,
            txs_gas_data=txs_gas_data,
        )
        
        ## Write the result to a JSON file for loading in the future
        write_json(block)

        return block


def _get_cache_path(block_number: int) -> Path:
    cache_directory_path = Path(cache_directory)
    return cache_directory_path / f"{block_number}-new.json"
