from typing import List, Tuple

from pydantic import BaseModel


class CoinbasePricesEntry(BaseModel):
    # tuple of price and timestamp
    prices: List[Tuple[float, int]]


class CoinbasePrices(BaseModel):
    all: CoinbasePricesEntry


class CoinbasePricesDataResponse(BaseModel):
    prices: CoinbasePrices


class CoinbasePricesResponse(BaseModel):
    data: CoinbasePricesDataResponse
