import json
import os

from mev_inspect.schemas.blocks import Block


THIS_FILE_DIRECTORY = os.path.dirname(__file__)
TEST_BLOCKS_DIRECTORY = os.path.join(THIS_FILE_DIRECTORY, "blocks")


def load_test_block(block_number: int) -> Block:
    block_path = f"{TEST_BLOCKS_DIRECTORY}/{block_number}.json"

    with open(block_path, "r") as block_file:
        block_json = json.load(block_file)
        return Block(**block_json)
