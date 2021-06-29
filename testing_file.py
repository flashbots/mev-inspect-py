from web3.providers import base
from inspector_uniswap import UniswapInspector
import block
from web3 import Web3
import argparse

parser = argparse.ArgumentParser(description='Inspect some blocks.')
parser.add_argument('-block_number', metavar='b', type=int, nargs='+',
                    help='the block number you are targetting, eventually this will need to be changed')
parser.add_argument('-rpc', metavar='r', help='rpc endpoint, this needs to have parity style traces')
args = parser.parse_args()

## Set up the base provider, but don't wrap it in web3 so we can make requests to it with make_request()
base_provider = Web3.HTTPProvider(args.rpc)

## Get block data that we need
block_data = block.createFromBlockNumber(args.block_number[0], base_provider)

## Build a Uniswap inspector
uniswap_inspector = UniswapInspector(base_provider)