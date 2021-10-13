import json
import os
from typing import Dict

from mev_inspect.schemas.blocks import Block


THIS_FILE_DIRECTORY = os.path.dirname(__file__)
TEST_BLOCKS_DIRECTORY = os.path.join(THIS_FILE_DIRECTORY, "blocks")


def load_test_block(block_number: int) -> Block:
    block_path = f"{TEST_BLOCKS_DIRECTORY}/{block_number}.json"

    with open(block_path, "r") as block_file:
        block_json = json.load(block_file)
        return Block(**block_json)


def load_comp_markets() -> Dict[str, str]:
    comp_markets_path = f"{THIS_FILE_DIRECTORY}/comp_markets.json"
    with open(comp_markets_path, "r") as markets_file:
        markets = json.load(markets_file)
        return markets
