from web3 import Web3
import configparser
import json

## Config file is used for addresses/ABIs
config = configparser.ConfigParser()
config.read('./utils/config.ini')

uniswap_router_abi = json.loads(config['ABI']['UniswapV2Router'])

class UniswapInspector:
    def __init__(self, base_provider) -> None:
        self.w3 = Web3(base_provider)
        self.trading_functions = self.get_trading_functions()
        self.uniswapV2RouterContract = self.w3.eth.contract(abi=uniswap_router_abi, address=config['ADDRESSES']['UniswapV2Router'])

    def get_trading_functions(self):
        ## Gets all functions used for swapping
        result = []
       
        for abi in uniswap_router_abi:
            if abi['type'] == 'function' and abi['name'].startswith('swap'):
                result.append(abi['name'])
        
        return result