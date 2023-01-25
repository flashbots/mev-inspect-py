import datetime
from time import sleep

import pandas as pd
from profit_analysis.column_names import BLOCK_KEY, TIMESTAMP_KEY


def add_block_timestamp(w3, profit_by_block):
    block_timestamp = pd.DataFrame(
        profit_by_block[BLOCK_KEY].unique(), columns=[BLOCK_KEY]
    )
    block_timestamp[TIMESTAMP_KEY] = block_timestamp[BLOCK_KEY].apply(
        lambda x: get_block_timestamp(w3, x)
    )
    return profit_by_block.merge(block_timestamp, on=BLOCK_KEY)


def get_block_timestamp(w3, block):
    while True:
        try:
            block_info = w3.eth.get_block(int(block))
            ts = block_info[TIMESTAMP_KEY]
            dt = datetime.datetime.fromtimestamp(ts)

            return dt
        except Exception as e:
            print(f"Error, retrying {e}")
            sleep(0.05)
