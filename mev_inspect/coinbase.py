import aiohttp

from mev_inspect.classifiers.specs.weth import WETH_ADDRESS
from mev_inspect.schemas.transfers import ETH_TOKEN_ADDRESS
from mev_inspect.schemas.coinbase import CoinbasePrices, CoinbasePricesResponse


COINBASE_API_BASE = "https://www.coinbase.com/api/v2"
COINBASE_TOKEN_NAME_BY_ADDRESS = {
    WETH_ADDRESS: "weth",
    ETH_TOKEN_ADDRESS: "ethereum",
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
