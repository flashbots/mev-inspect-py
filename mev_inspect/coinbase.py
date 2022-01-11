import aiohttp

from mev_inspect.classifiers.specs.weth import WETH_ADDRESS
from mev_inspect.schemas.coinbase import CoinbasePrices, CoinbasePricesResponse
from mev_inspect.schemas.prices import (
    AAVE_TOKEN_ADDRESS,
    CDAI_TOKEN_ADDRESS,
    CUSDC_TOKEN_ADDRESS,
    DAI_TOKEN_ADDRESS,
    LINK_TOKEN_ADDRESS,
    REN_TOKEN_ADDRESS,
    UNI_TOKEN_ADDRESS,
    USDC_TOKEN_ADDRESS,
    WBTC_TOKEN_ADDRESS,
    YEARN_TOKEN_ADDRESS,
)
from mev_inspect.schemas.transfers import ETH_TOKEN_ADDRESS

COINBASE_API_BASE = "https://www.coinbase.com/api/v2"
COINBASE_TOKEN_NAME_BY_ADDRESS = {
    WETH_ADDRESS: "weth",
    ETH_TOKEN_ADDRESS: "ethereum",
    WBTC_TOKEN_ADDRESS: "wrapped-bitcoin",
    LINK_TOKEN_ADDRESS: "chainlink",
    YEARN_TOKEN_ADDRESS: "yearn-finance",
    AAVE_TOKEN_ADDRESS: "aave",
    UNI_TOKEN_ADDRESS: "uniswap",
    USDC_TOKEN_ADDRESS: "usdc",
    DAI_TOKEN_ADDRESS: "dai",
    REN_TOKEN_ADDRESS: "ren",
    CUSDC_TOKEN_ADDRESS: "compound-usd-coin",
    CDAI_TOKEN_ADDRESS: "compound-dai",
}


async def fetch_coinbase_prices(token_address: str) -> CoinbasePrices:
    if token_address not in COINBASE_TOKEN_NAME_BY_ADDRESS:
        raise ValueError(f"Unsupported token_address {token_address}")

    coinbase_token_name = COINBASE_TOKEN_NAME_BY_ADDRESS[token_address]
    url = f"{COINBASE_API_BASE}/assets/prices/{coinbase_token_name}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={"base": "USD"}) as response:
            json_data = await response.json()
            return CoinbasePricesResponse(**json_data).data.prices
