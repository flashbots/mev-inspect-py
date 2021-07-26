import argparse
import json

from web3 import Web3

from mev_inspect import block
from mev_inspect.processor import Processor
from mev_inspect.schemas.classifications import Classification, DecodeSpec, Protocol


SUSHISWAP_ROUTER_ADDRESS = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
UNISWAP_V2_ROUTER_ADDRESS = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"


DECODE_SPECS = [
    DecodeSpec(
        abi_name="UniswapV2Router",
        protocol=Protocol.uniswap_v2,
        valid_contract_addresses=[UNISWAP_V2_ROUTER_ADDRESS],
    ),
    DecodeSpec(
        abi_name="UniswapV2Router",
        protocol=Protocol.sushiswap,
        valid_contract_addresses=[SUSHISWAP_ROUTER_ADDRESS],
    ),
    DecodeSpec(
        abi_name="ERC20",
        classifications={
            "transferFrom(address,address,uint256)": Classification.transfer,
            "transfer(address,uint256)": Classification.transfer,
            "burn(address)": Classification.burn,
        },
    ),
    DecodeSpec(
        abi_name="UniswapV2Pair",
        classifications={
            "swap(uint256,uint256,address,bytes)": Classification.swap,
        },
    ),
]


def inspect_block(base_provider, block_number):
    print("Using decode specs:")

    for spec in DECODE_SPECS:
        print(spec.json(indent=4, exclude_unset=True))

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

    processor = Processor(DECODE_SPECS)
    classified_traces = processor.process(block_data)

    print(f"Returned {len(classified_traces)} classified traces")

    stats = {}

    for trace in classified_traces:
        abi_name = trace.abi_name
        classification = trace.classification.value
        signature = trace.function_signature

        abi_name_stats = stats.get(abi_name, {})
        class_stats = abi_name_stats.get(classification, {})
        signature_count = abi_name_stats.get(signature, 0)
        class_stats[signature] = signature_count + 1
        abi_name_stats[classification] = class_stats
        stats[abi_name] = abi_name_stats

    print(json.dumps(dict(stats.items()), indent=4))


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
