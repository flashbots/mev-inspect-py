import json
from typing import Optional

from web3 import Web3

from mev_inspect.config import load_config
from mev_inspect.schemas.blocks import NestedTrace
from mev_inspect.schemas.classifications import Classification, Liquidation
from mev_inspect.utils import check_trace_for_signature

from .base import Inspector

config = load_config()

aave_v2_lending_pool_abi = json.loads(config["ABI"]["AaveLendingPool"])
aave_v2_lending_pool_address = config["ADDRESSES"]["AaveV2LendingPool"].lower()


class AaveInspector(Inspector):
    def __init__(self, base_inspector):
        super().__init__()
        self.w3 = Web3(base_inspector)
        self.aave_v2_lendingpool_contract = self.w3.eth.contract(
            address=aave_v2_lending_pool_address, abi=aave_v2_lending_pool_abi
        )

        # https://docs.aave.com/developers/the-core-protocol/lendingpool#liquidationcall
        liquidation_call = "liquidationCall(address,address,address,uint256,bool)"
        self.liquidation_call_signature = self.w3.sha3(text=liquidation_call)[:4]
        self.mev_functions = []

    def inspect(self, nested_trace: NestedTrace) -> Optional[Classification]:
        trace = nested_trace.trace

        # fmt: off
        if (
            trace.action["to"] == aave_v2_lending_pool_address and
            check_trace_for_signature(
                trace,
                [self.liquidation_call_signature]
            )
        ):
        # fmt: on

            tx = self.w3.eth.get_transaction(trace.transaction_hash)
            _, decoded_input = self.aave_v2_lendingpool_contract.decode_function_input(tx.input)
            print(decoded_input)

            # TODO: check if decoded_input is correct, create a Liquidation classification?
            #       what about reducers?
            # return Liquidation()

        return None
