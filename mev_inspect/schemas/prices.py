from datetime import datetime

from pydantic import BaseModel, validator

ETH_TOKEN_ADDRESS = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
WETH_TOKEN_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
WBTC_TOKEN_ADDRESS = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"
LINK_TOKEN_ADDRESS = "0x514910771af9ca656af840dff83e8264ecf986ca"
YEARN_TOKEN_ADDRESS = "0x0bc529c00c6401aef6d220be8c6ea1667f6ad93e"
AAVE_TOKEN_ADDRESS = "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9"
UNI_TOKEN_ADDRESS = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"
USDC_TOKEN_ADDRESS = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
DAI_TOKEN_ADDRESS = "0x6b175474e89094c44da98b954eedeac495271d0f"
REN_TOKEN_ADDRESS = "0x408e41876cccdc0f92210600ef50372656052a38"
CUSDC_TOKEN_ADDRESS = "0x39aa39c021dfbae8fac545936693ac917d5e7563"
CDAI_TOKEN_ADDRESS = "0x5d3a536e4d6dbd6114cc1ead35777bab948e3643"
CETH_TOKEN_ADDRESS = "0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5"
CWBTC_TOKEN_ADDRESS = "0xc11b1268c1a384e55c48c2391d8d480264a3a7f4"

TOKEN_ADDRESSES = [
    ETH_TOKEN_ADDRESS,
    WETH_TOKEN_ADDRESS,
    WBTC_TOKEN_ADDRESS,
    LINK_TOKEN_ADDRESS,
    YEARN_TOKEN_ADDRESS,
    AAVE_TOKEN_ADDRESS,
    UNI_TOKEN_ADDRESS,
    USDC_TOKEN_ADDRESS,
    DAI_TOKEN_ADDRESS,
    REN_TOKEN_ADDRESS,
    CUSDC_TOKEN_ADDRESS,
    CDAI_TOKEN_ADDRESS,
    CETH_TOKEN_ADDRESS,
    CWBTC_TOKEN_ADDRESS,
]

COINGECKO_ID_BY_ADDRESS = {
    WETH_TOKEN_ADDRESS: "weth",
    ETH_TOKEN_ADDRESS: "ethereum",
    WBTC_TOKEN_ADDRESS: "wrapped-bitcoin",
    LINK_TOKEN_ADDRESS: "chainlink",
    YEARN_TOKEN_ADDRESS: "yearn-finance",
    AAVE_TOKEN_ADDRESS: "aave",
    UNI_TOKEN_ADDRESS: "uniswap",
    USDC_TOKEN_ADDRESS: "usd-coin",
    DAI_TOKEN_ADDRESS: "dai",
    REN_TOKEN_ADDRESS: "republic-protocol",
    CUSDC_TOKEN_ADDRESS: "compound-usd-coin",
    CDAI_TOKEN_ADDRESS: "cdai",
    CETH_TOKEN_ADDRESS: "compound-ether",
    CWBTC_TOKEN_ADDRESS: "compound-wrapped-btc",
}


class Price(BaseModel):
    token_address: str
    usd_price: float
    timestamp: datetime

    @validator("token_address")
    def lower_token_address(cls, v: str) -> str:
        return v.lower()
