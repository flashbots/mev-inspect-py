import block
test_block_num = 12412732

block_data = block.createFromBlockNumber(test_block_num)

for transaction_hash in block_data.transaction_hashes:
    calls = block_data.get_filtered_calls(transaction_hash)
    print(calls)