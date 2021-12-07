import aiohttp

from mev_inspect.classifiers.specs.weth import WETH_ADDRESS
from mev_inspect.schemas.transfers import ETH_TOKEN_ADDRESS
from mev_inspect.schemas.coinbase import CoinbasePrices, CoinbasePricesResponse

WBTC_TOKEN_ADDRESS = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"
LINK_TOKEN_ADDRESS = "0x514910771af9ca656af840dff83e8264ecf986ca"
YEARN_TOKEN_ADDRESS = "0x0bc529c00c6401aef6d220be8c6ea1667f6ad93e"
AAVE_TOKEN_ADDRESS = "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9"
UNI_TOKEN_ADDRESS = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"
USDC_TOKEN_ADDRESS_ADDRESS = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
REN_TOKEN_ADDRESS = "0x408e41876cccdc0f92210600ef50372656052a38"
SUSHIBAR_TOKEN_ADDRESS = "0x8798249c2e607446efb7ad49ec89dd1865ff4272"

COINBASE_API_BASE = "https://www.coinbase.com/api/v2"
COINBASE_TOKEN_NAME_BY_ADDRESS = {
    WETH_ADDRESS: "weth",
    ETH_TOKEN_ADDRESS: "ethereum",
    WBTC_TOKEN_ADDRESS: "wbtc",
    LINK_TOKEN_ADDRESS: "link",
    YEARN_TOKEN_ADDRESS: "yearn",
    AAVE_TOKEN_ADDRESS: "aave",
    UNI_TOKEN_ADDRESS: "uni",
    USDC_TOKEN_ADDRESS_ADDRESS: "usdc",
    REN_TOKEN_ADDRESS: "ren",
    SUSHIBAR_TOKEN_ADDRESS: "sushibar",
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
