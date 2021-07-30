from typing import List

from mev_inspect.schemas.classified_traces import ClassifiedTrace
from mev_inspect.schemas.strategies import Arbitrage


def get_arbitrages(traces: List[ClassifiedTrace]) -> List[Arbitrage]:
    return []
