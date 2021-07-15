import json

from web3 import Web3

from mev_inspect import utils
from mev_inspect.config import load_config

config = load_config()

uniswap_router_abi = json.loads(config["ABI"]["UniswapV2Router"])
uniswap_router_address = config["ADDRESSES"]["UniswapV2Router"]
sushiswap_router_address = config["ADDRESSES"]["SushiswapV2Router"]

uniswap_pair_abi = json.loads(config["ABI"]["UniswapV2Pair"])


class UniswapInspector:
    def __init__(self, base_provider) -> None:
        self.w3 = Web3(base_provider)

        self.trading_functions = self.get_trading_functions()
        self.uniswap_v2_router_contract = self.w3.eth.contract(
            abi=uniswap_router_abi, address=uniswap_router_address
        )
        self.uniswap_router_trade_signatures = self.get_router_signatures()

        self.uniswap_v2_pair_contract = self.w3.eth.contract(abi=uniswap_pair_abi)
        self.uniswap_v2_pair_swap_signatures = (
            self.uniswap_v2_pair_contract.functions.swap(
                0, 0, uniswap_router_address, ""
            ).selector
        )  ## Note the address here doesn't matter, but it must be filled out
        self.uniswap_v2_pair_reserves_signatures = (
            self.uniswap_v2_pair_contract.functions.getReserves().selector
        )  ## Called "checksigs" in mev-inpsect.ts

        print("Built Uniswap inspector")

    def get_trading_functions(self):
        ## Gets all functions used for swapping
        result = []

        ## For each entry in the ABI
        for abi in uniswap_router_abi:
            ## Check to see if the entry is a function and if it is if the function's name starts with swap
            if abi["type"] == "function" and abi["name"].startswith("swap"):
                ## If so add it to our array
                result.append(abi["name"])

        return result

    def get_router_signatures(self):
        ## Gets the selector / function signatures of all the router swap functions
        result = []

        ## For each entry in the ABI
        for abi in uniswap_router_abi:
            ## Check to see if the entry is a function and if it is if the function's name starts with swap
            if abi["type"] == "function" and abi["name"].startswith("swap"):
                ## Add a parantheses
                function = abi["name"] + "("

                ## For each input in the function's input
                for input in abi["inputs"]:

                    ## Concat them into a string with commas
                    function = function + input["internalType"] + ","

                ## Take off the last comma, add a ')' to close the parentheses
                function = function[:-1] + ")"

                ## The result looks like this: 'swapETHForExactTokens(uint256,address[],address,uint256)'

                ## Take the first 4 bytes of the sha3 hash of the above string.
                selector = Web3.sha3(text=function)[0:4]

                ## Add that to an array
                result.append(selector)

        return result

    def inspect(self, calls):
        for call in calls:
            print("\n", call)
            if (
                call["action"]["to"] == uniswap_router_address.lower()
                or call["action"]["to"] == sushiswap_router_address.lower()
            ) and utils.check_call_for_signature(
                call, self.uniswap_router_trade_signatures
            ):
                # print("WIP, here is where there is a call that matches what we are looking for")
                1 == 1
