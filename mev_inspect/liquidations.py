from typing import List

from web3 import Web3
from mev_inspect.aave_liquidations import get_aave_liquidations
from mev_inspect.compound_liquidations import (
    get_compound_liquidations,
    fetch_all_underlying_markets,
)
from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    Classification,
    Protocol,
)
from mev_inspect.schemas.liquidations import Liquidation


def has_liquidations(classified_traces: List[ClassifiedTrace]) -> bool:
    liquidations_exist = False
    for classified_trace in classified_traces:
        if classified_trace.classification == Classification.liquidate:
            liquidations_exist = True
    return liquidations_exist


def get_liquidations(
    classified_traces: List[ClassifiedTrace], w3: Web3
) -> List[Liquidation]:
    # to avoid contract calls to fetch comp/cream markets
    # unless there is a liquidation

    if has_liquidations(classified_traces):
        aave_liquidations = get_aave_liquidations(classified_traces)
        comp_markets = fetch_all_underlying_markets(w3, Protocol.compound_v2)
        cream_markets = fetch_all_underlying_markets(w3, Protocol.cream)
        compound_liquidations = get_compound_liquidations(
            classified_traces, comp_markets, cream_markets
        )
        return aave_liquidations + compound_liquidations

    return []
