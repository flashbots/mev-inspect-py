from unittest.mock import MagicMock, patch

import pytest

from mev_inspect.block import _find_or_fetch_miner_address
from tests.utils import load_test_block


# Set up generic mock for web3
@pytest.fixture
def mocked_web3():
    with patch("mev_inspect.block.Web3") as mock_web3:
        yield mock_web3


@pytest.mark.asyncio
# pylint: disable=redefined-outer-name
async def test_eth1_block_miner(mocked_web3):

    # instantiate the mock
    mock_web3_instance = mocked_web3.return_value
    mock_eth = mock_web3_instance.eth
    mock_eth.get_block.return_value = {
        "miner": "0x4a536c1f6a5d5a9c1aeca9f6d04fbbf5f0d8f4e3"
    }

    # load a sample block and remove the miner
    block_number = 10921991
    block = load_test_block(block_number)
    block.miner = None

    # test that the miner is fetched
    miner_address = await _find_or_fetch_miner_address(
        w3=mock_web3_instance, traces=block.traces, block_number=block_number
    )  # Use 'await'

    # test it is fetched from traces object
    assert miner_address == "0x52bc44d5378309ee2abf1539bf71de1b7d7be3b5"


@pytest.mark.asyncio
# pylint: disable=redefined-outer-name
async def test_eth2_block_miner(mocked_web3):
    # instantiate the mock
    mock_web3_instance = mocked_web3.return_value
    # pylint: disable=unused-argument
    async def mock_get_block(block_number):
        return {"miner": "0x4a536c1f6a5d5a9c1aeca9f6d04fbbf5f0d8f4e3"}

    mock_web3_instance.eth.get_block = MagicMock(side_effect=mock_get_block)

    # load a sample block and remove the miner
    block_number = 10921990
    block = load_test_block(block_number)
    block.miner = None

    # test that the miner is fetched
    miner_address = await _find_or_fetch_miner_address(
        w3=mock_web3_instance, traces=block.traces, block_number=block_number
    )

    # test miner is fectched from mocked object
    assert miner_address == "0x4a536c1f6a5d5a9c1aeca9f6d04fbbf5f0d8f4e3"
