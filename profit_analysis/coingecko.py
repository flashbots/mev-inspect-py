import pandas as pd
import pycoingecko as pg
from profit_analysis.column_names import (
    CG_ID_DEBT_KEY,
    CG_ID_KEY,
    CG_ID_RECEIVED_KEY,
    PRICE_KEY,
    TIMESTAMP_KEY,
    TOKEN_DEBT_KEY,
    TOKEN_KEY,
    TOKEN_RECEIVED_KEY,
)
from profit_analysis.constants import DATA_PATH

TRAILING_ZEROS = "000000000000000000000000"


def get_address_to_coingecko_ids_mapping(chain):
    token_cg_ids = pd.read_csv(DATA_PATH + "address_to_coingecko_ids.csv")
    token_cg_ids = token_cg_ids.loc[token_cg_ids["chain"] == chain]
    token_cg_ids[TOKEN_DEBT_KEY] = token_cg_ids[TOKEN_KEY].astype(str)
    token_cg_ids[CG_ID_RECEIVED_KEY] = token_cg_ids[CG_ID_KEY]
    token_cg_ids[CG_ID_DEBT_KEY] = token_cg_ids[CG_ID_KEY]
    token_cg_ids[TOKEN_RECEIVED_KEY] = token_cg_ids[TOKEN_KEY].astype(str)
    return token_cg_ids


def add_cg_ids(profit_by_block, chain):
    token_cg_ids = get_address_to_coingecko_ids_mapping(chain)
    token_cg_ids[TOKEN_DEBT_KEY] = token_cg_ids[TOKEN_DEBT_KEY].str.lower()
    token_cg_ids[TOKEN_RECEIVED_KEY] = token_cg_ids[TOKEN_RECEIVED_KEY].str.lower()
    profit_by_block[TOKEN_RECEIVED_KEY] = (
        profit_by_block[TOKEN_RECEIVED_KEY]
        .map(lambda x: x.replace(TRAILING_ZEROS, ""))
        .str.lower()
    )
    profit_by_block[TOKEN_DEBT_KEY] = (
        profit_by_block[TOKEN_DEBT_KEY]
        .map(lambda x: x.replace(TRAILING_ZEROS, ""))
        .str.lower()
    )
    profit_by_block = profit_by_block.merge(
        token_cg_ids[[TOKEN_DEBT_KEY, CG_ID_DEBT_KEY]], on=TOKEN_DEBT_KEY, how="left"
    )
    profit_by_block = profit_by_block.merge(
        token_cg_ids[[TOKEN_RECEIVED_KEY, CG_ID_RECEIVED_KEY]], how="left"
    )
    addresses_with_nan_cg_ids = profit_by_block.loc[
        pd.isna(profit_by_block[CG_ID_RECEIVED_KEY]), TOKEN_RECEIVED_KEY
    ]
    print(
        f"Tokens with missing coingecko ids in mapping:\n{addresses_with_nan_cg_ids.value_counts()}"
    )
    return profit_by_block[
        [
            "block_number",
            "timestamp",
            "transaction_hash",
            "token_debt",
            "amount_debt",
            "cg_id_debt",
            "token_received",
            "amount_received",
            "cg_id_received",
        ]
    ]


def get_coingecko_historical_prices(start, end, token):
    cg = pg.CoinGeckoAPI()
    token_prices = cg.get_coin_market_chart_range_by_id(
        id=token, vs_currency="usd", from_timestamp=start, to_timestamp=end
    )["prices"]
    token_prices = pd.DataFrame(token_prices, columns=[TIMESTAMP_KEY, PRICE_KEY])
    token_prices[TIMESTAMP_KEY] = pd.to_datetime(
        pd.to_numeric(token_prices[TIMESTAMP_KEY]), unit="ms"
    )
    return token_prices[[TIMESTAMP_KEY, PRICE_KEY]]
