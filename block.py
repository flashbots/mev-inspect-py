from web3 import Web3
from pathlib import Path
import json

rpc_end_point = ""
base_provider = Web3.HTTPProvider(rpc_end_point)
w3 = Web3(base_provider)

cache_directoty = './cache'

class BlockData:
    def __init__(self, block_number, data, receipts, calls, logs) -> None:
        self.block_number = block_number
        self.data = data
        self.receipts = receipts
        self.calls = calls
        self.logs = logs
        self.transaction_hashes = self.get_transaction_hashes()
        pass
    
    ## Gets a list of unique transasction hashes in the calls of this block
    def get_transaction_hashes(self):
        result = []
        for call in self.calls:
            if call['type'] != 'reward':
                if call['transactionHash'] in result:
                    continue
                else: 
                    result.append(call['transactionHash'])
        
        return result

    ## Makes a nicely formatted JSON object out of this data object.
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    ## Writes this object to a JSON file for loading later
    def writeJSON(self):
        json_data = self.toJSON()
        cache_file = '{cacheDirectory}/{blockNumber}.json'.format(cacheDirectory=cache_directoty, blockNumber=self.block_number)
        file_exists = Path(cache_file).is_file()
        if file_exists:
            f = open(cache_file, "w")
            f.write(json_data)
            f.close()
        else:
            f = open(cache_file, "x")
            f.write(json_data)
            f.close()
    
    ## Gets all the calls associated with a transaction hash
    def get_filtered_calls(self, hash):
        result = []

        for call in self.calls:
            if call['transactionHash'] == hash:
                result.append(call)
        
        return result


## Creates a block object, either from the cache or from the chain itself
def createFromBlockNumber(block_number):
    cache_file = '{cacheDirectory}/{blockNumber}.json'.format(cacheDirectory=cache_directoty, blockNumber=block_number)
    
    ## Check to see if the data already exists in the cache
    ## if it exists load the data from cache
    ## If not then get the data from the chain and save it to the cache
    if (Path(cache_file).is_file()):
        print("Cache for this block exists, loading again")
        block_file = open(cache_file)
        block_json = json.load(block_file)
        block = BlockData(block_number, block_json['data'], block_json['receipts'], block_json['calls'], block_json['logs'])
        return block
    else:
        print("Cache for this block did not exist, getting data")
        
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
        
        ## Create a new object
        block = BlockData(block_number, block_data, block_receipts_raw, block_calls, block_logs)
        
        ## Write the result to a JSON file for loading in the future
        block.writeJSON()
        return block