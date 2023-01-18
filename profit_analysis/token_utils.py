import pandas as pd
from profit_analysis.column_names import TOKEN_KEY
from profit_analysis.constants import DATA_PATH


def get_decimals(token_address, chain):
    decimals_mapping = pd.read_csv(DATA_PATH + "address_to_decimals.csv")
    decimals_mapping = decimals_mapping.loc[decimals_mapping["chain"] == chain]
    decimals_mapping[TOKEN_KEY] = decimals_mapping[TOKEN_KEY].str.lower()
    decimals = decimals_mapping.loc[
        decimals_mapping[TOKEN_KEY] == token_address.lower(), "decimals"
    ].values
    if len(decimals) > 0:
        return decimals[0]
    else:
        raise Exception("No Decimals for token=", token_address)
