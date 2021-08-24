from mev_inspect.schemas.classified_traces import Protocol
from mev_inspect.abi import get_raw_abi
from web3 import Web3

rpc = ""
w3 = Web3(Web3.HTTPProvider(rpc))


weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
usdc_address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
zero_address = "0x0000000000000000000000000000000000000000"

uniswap_router = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
uniswap_factory = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
sushiswap_router = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
sushiswap_factory = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"

router_abi = get_raw_abi("UniswapV2Router", Protocol.uniswap_v2)
factory_abi = get_raw_abi("UniswapV2Factory", Protocol.uniswap_v2)
pool_abi = get_raw_abi("UniswapV2Pair", None)

# helper to get decimals of any given erc20 token
def get_erc20_token_decimals(token_address):
    token_abi = get_raw_abi("ERC20", None)
    token_instance = w3.eth.contract(address=token_address, abi=token_abi)
    decimals = token_instance.functions.decimals().call()
    return decimals


# get the specific uniswap/sushiswap pools for a pair of tokens
def get_uniswap_pair_pool(token_0, token_1):
    factory_instance = w3.eth.contract(address=uniswap_factory, abi=factory_abi)
    pair_address = factory_instance.functions.getPair(token_0, token_1).call()
    # 0x0 is returned when the pair does not have a pool
    if pair_address != zero_address:
        return pair_address
    else:
        return None


def get_sushiswap_pair_pool(token_0, token_1):
    factory_instance = w3.eth.contract(address=sushiswap_factory, abi=factory_abi)
    pair_address = factory_instance.functions.getPair(token_0, token_1).call()
    # 0x0 is returned when the pair does not have a pool
    if pair_address != zero_address:
        return pair_address
    else:
        return None


# get reserves of a pool at a specific block number
def get_uni_pool_reserves(pool_address, block_number):
    pool_instance = w3.eth.contract(address=pool_address, abi=pool_abi)
    token_0 = pool_instance.functions.token0().call()
    token_1 = pool_instance.functions.token1().call()
    token_0_reserve, token_1_reserve, _ = pool_instance.functions.getReserves().call(
        block_identifier=block_number
    )
    return {token_0: token_0_reserve, token_1: token_1_reserve}


def get_sushi_pool_reserves(pool_address, block_number):
    pool_instance = w3.eth.contract(address=pool_address, abi=pool_abi)
    token_0 = pool_instance.functions.token0().call()
    token_1 = pool_instance.functions.token1().call()
    token_0_reserve, token_1_reserve, _ = pool_instance.functions.getReserves().call(
        block_identifier=block_number
    )
    return {token_0: token_0_reserve, token_1: token_1_reserve}


# get the price of any token (in eth) at a specific block number
def get_erc20_token_price_in_eth(token_amount, token_address, block_number):
    # get the TOKEN-ETH pool addresses from AMM factory
    uni_pair_pool_address = get_uniswap_pair_pool(token_address, weth_address)
    sushi_pair_pool_address = get_sushiswap_pair_pool(token_address, weth_address)

    # get reserves from both pools, to pick one with greater liquidity at that block height
    uni_pool_reserves = get_uni_pool_reserves(uni_pair_pool_address, block_number)
    sushi_pool_reserves = get_sushi_pool_reserves(sushi_pair_pool_address, block_number)

    # if uniswap has better liquidity
    if uni_pool_reserves[token_address] > sushi_pool_reserves[token_address]:
        router_instance = w3.eth.contract(address=uniswap_router, abi=router_abi)
        token_price_in_wei = router_instance.functions.getAmountOut(
            token_amount,
            uni_pool_reserves[token_address],
            uni_pool_reserves[weth_address],
        ).call()
        token_price_in_eth = w3.fromWei(token_price_in_wei, "ether")
        return token_price_in_eth
    else:  # sushiswap has better liquidity
        router_instance = w3.eth.contract(address=sushiswap_router, abi=router_abi)
        token_price_in_wei = router_instance.functions.getAmountOut(
            token_amount,
            sushi_pool_reserves[token_address],
            sushi_pool_reserves[weth_address],
        ).call()
        token_price_in_eth = w3.fromWei(token_price_in_wei, "ether")
        return token_price_in_eth


# same but denominated in USDC
def get_erc20_token_price_in_usdc(token_amount, token_address, block_number):
    # get the TOKEN-ETH pool addresses from AMM factory
    uni_pair_pool_address = get_uniswap_pair_pool(token_address, usdc_address)
    sushi_pair_pool_address = get_sushiswap_pair_pool(token_address, usdc_address)

    # get reserves from both pools, to pick one with greater liquidity at that block height
    uni_pool_reserves = get_uni_pool_reserves(uni_pair_pool_address, block_number)
    sushi_pool_reserves = get_sushi_pool_reserves(sushi_pair_pool_address, block_number)

    # if uniswap has better liquidity
    if uni_pool_reserves[token_address] > sushi_pool_reserves[token_address]:
        router_instance = w3.eth.contract(address=uniswap_router, abi=router_abi)
        token_price = router_instance.functions.getAmountOut(
            token_amount,
            uni_pool_reserves[token_address],
            uni_pool_reserves[usdc_address],
        ).call()
        # usdc has 6 decimals
        return token_price / 10 ** 6
    else:  # sushiswap has better liquidity
        router_instance = w3.eth.contract(address=sushiswap_router, abi=router_abi)
        token_price = router_instance.functions.getAmountOut(
            token_amount,
            sushi_pool_reserves[token_address],
            sushi_pool_reserves[usdc_address],
        ).call()
        return token_price / 10 ** 6
