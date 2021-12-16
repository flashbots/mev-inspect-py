from datetime import datetime

from pydantic import BaseModel, validator

WBTC_TOKEN_ADDRESS = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"
LINK_TOKEN_ADDRESS = "0x514910771af9ca656af840dff83e8264ecf986ca"
YEARN_TOKEN_ADDRESS = "0x0bc529c00c6401aef6d220be8c6ea1667f6ad93e"
AAVE_TOKEN_ADDRESS = "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9"
UNI_TOKEN_ADDRESS = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"
USDC_TOKEN_ADDRESS_ADDRESS = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
REN_TOKEN_ADDRESS = "0x408e41876cccdc0f92210600ef50372656052a38"


class Price(BaseModel):
    token_address: str
    timestamp: datetime
    usd_price: float

    @validator("token_address")
    def lower_token_address(cls, v: str) -> str:
        return v.lower()
