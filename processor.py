

def get_transaction_evaluations(block_data):
    for transaction_hash in block_data.transaction_hashes:
        calls = block_data.get_filtered_calls(transaction_hash)
        print(calls)