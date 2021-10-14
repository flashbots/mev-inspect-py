from typing import List

from web3 import Web3
from mev_inspect.aave_liquidations import get_aave_liquidations
from mev_inspect.compound_liquidations import (
    get_compound_liquidations,
    fetch_all_comp_markets,
)
from mev_inspect.schemas.classified_traces import ClassifiedTrace
from mev_inspect.schemas.liquidations import Liquidation


def get_liquidations(
    classified_traces: List[ClassifiedTrace], w3: Web3
) -> List[Liquidation]:
    aave_liquidations = get_aave_liquidations(classified_traces)
    comp_markets = fetch_all_comp_markets(w3)
    compound_liquidations = get_compound_liquidations(classified_traces, comp_markets)
    return aave_liquidations + compound_liquidations
