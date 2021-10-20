from web3 import Web3


async def fetch_base_fee_per_gas(w3: Web3, block_number: int) -> int:
    base_fees = await w3.eth.fee_history(1, block_number)
    base_fees_per_gas = base_fees["baseFeePerGas"]
    if len(base_fees_per_gas) == 0:
        raise RuntimeError("Unexpected error - no fees returned")

    return base_fees_per_gas[0]
