import sys

from profit_analysis.analysis import analyze_profit, get_profit_by
from profit_analysis.column_names import BLOCK_KEY

from mev_inspect.db import get_inspect_session

block_from = int(sys.argv[1])
block_to = int(sys.argv[2])
inspect_db_session = get_inspect_session()
profit = analyze_profit(inspect_db_session, block_from, block_to, True)
print("    -------------------------------------------------------------------")
print("    Profit By Block")
print(get_profit_by(profit, BLOCK_KEY, True))
print("    -------------------------------------------------------------------")
print("    Profit By Day")
print(get_profit_by(profit, "date", True))
print("    -------------------------------------------------------------------")
print("    Profit By Category")
print(get_profit_by(profit, "category", True))
