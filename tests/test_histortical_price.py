from mev_inspect.historical_price import (
    get_erc20_token_price_in_eth,
    get_erc20_token_price_in_usdc,
    get_erc20_token_decimals,
)


rpc = os.getenv("RPC_URL")

if rpc is None:
    raise RuntimeError("Missing environment variable RPC_URL")
else:
    w3 = Web3(Web3.HTTPProvider(rpc))

def test_historical_price():
    uni_token_address = "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
    uni_decimals = get_erc20_token_decimals(uni_token_address)
    uni_amount = 1 * (10 ** uni_decimals)
    block_number = 13320250
    historical_uni_price_in_eth = get_erc20_token_price_in_eth(
        uni_amount, uni_token_address, block_number, w3
    )
    historical_uni_price_in_usdc = get_erc20_token_price_in_usdc(
        uni_amount, uni_token_address, block_number, w3
    )
    assert (
        historical_uni_price_in_eth == 0.008136743925185488
    )  # prices at that block height
    assert historical_uni_price_in_usdc == 23.598414

    # ALCX and NFTX have more liquidity on sushiswap than uni
    alcx_token_address = "0xdBdb4d16EdA451D0503b854CF79D55697F90c8DF"
    alcx_decimals = get_erc20_token_decimals(alcx_token_address)
    alcx_amount = 1 * (10 ** alcx_decimals)
    historical_alcx_price_in_eth = get_erc20_token_price_in_eth(
        alcx_amount, alcx_token_address, block_number
    )
    historical_alcx_price_in_usdc = get_erc20_token_price_in_usdc(
        alcx_amount, alcx_token_address, block_number, w3
    )
    assert historical_alcx_price_in_eth == 0.074379006845621186
    assert (
        historical_alcx_price_in_usdc == 0
    )  # 0 because ALCX-USDC pair does not exist on sushiswap or uniswap

    nftx_token_address = "0x87d73E916D7057945c9BcD8cdd94e42A6F47f776"
    nftx_decimals = get_erc20_token_decimals(nftx_token_address)
    nftx_amount = 1 * (10 ** nftx_decimals)
    historical_nftx_price_in_eth = get_erc20_token_price_in_eth(
        nftx_amount, nftx_token_address, block_number, w3
    )
    historical_nftx_price_in_usdc = get_erc20_token_price_in_usdc(
        nftx_amount, nftx_token_address, block_number, w3
    )
    assert historical_nftx_price_in_eth == 0.045450080391748228
    assert historical_nftx_price_in_usdc == 0