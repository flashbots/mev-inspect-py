from typing import List

from mev_inspect.aave_liquidations import get_aave_liquidations
from mev_inspect.compound_liquidations import get_compound_liquidations
from mev_inspect.schemas.traces import (
    ClassifiedTrace,
    Classification,
)
from mev_inspect.schemas.liquidations import Liquidation


def has_liquidations(classified_traces: List[ClassifiedTrace]) -> bool:
    liquidations_exist = False
    for classified_trace in classified_traces:
        if classified_trace.classification == Classification.liquidate:
            liquidations_exist = True
    return liquidations_exist


def get_liquidations(
    classified_traces: List[ClassifiedTrace],
) -> List[Liquidation]:
    aave_liquidations = get_aave_liquidations(classified_traces)
    comp_liquidations = get_compound_liquidations(classified_traces)
    return aave_liquidations + comp_liquidations
