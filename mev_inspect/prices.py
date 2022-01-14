from datetime import datetime as dt
from typing import List

from pycoingecko import CoinGeckoAPI

from mev_inspect.schemas.prices import COINGECKO_ID_BY_ADDRESS, TOKEN_ADDRESSES, Price


def fetch_prices() -> List[Price]:
    cg = CoinGeckoAPI()
    prices = []

    for token_address in TOKEN_ADDRESSES:
        price_data = cg.get_coin_market_chart_by_id(
            id=COINGECKO_ID_BY_ADDRESS[token_address], vs_currency="usd", days="max"
        )
        price_time_series = price_data["prices"]

        for entry in price_time_series:
            timestamp = dt.fromtimestamp(entry[0] / 100)
            token_price = entry[1]
            prices.append(
                Price(
                    timestamp=timestamp,
                    usd_price=token_price,
                    token_address=token_address,
                )
            )

    return prices
