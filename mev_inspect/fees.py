from web3 import Web3


def fetch_base_fee_per_gas(w3: Web3, block_number: int) -> int:
    base_fees = w3.eth.fee_history(1, block_number)["baseFeePerGas"]
    if len(base_fees) == 0:
        raise RuntimeError("Unexpected error - no fees returned")

    return base_fees[0]
