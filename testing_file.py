import argparse

from web3 import Web3

from mev_inspect import block
from mev_inspect.processor import Processor


def inspect_block(base_provider, block_number):
    block_data = block.create_from_block_number(block_number, base_provider)
    print(f"Total traces: {len(block_data.traces)}")

    total_transactions = len(
        set(
            t.transaction_hash
            for t in block_data.traces
            if t.transaction_hash is not None
        )
    )
    print(f"Total transactions: {total_transactions}")

    processor = Processor()
    classifications = processor.process(block_data)

    print(f"Returned {len(classifications)} classifications")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inspect some blocks.")

    parser.add_argument(
        "-block_number",
        metavar="b",
        type=int,
        nargs="+",
        help="the block number you are targetting, eventually this will need to be changed",
    )

    parser.add_argument(
        "-rpc", metavar="r", help="rpc endpoint, this needs to have parity style traces"
    )

    args = parser.parse_args()

    w3_base_provider = Web3.HTTPProvider(args.rpc)
    inspect_block(w3_base_provider, args.block_number[0])
