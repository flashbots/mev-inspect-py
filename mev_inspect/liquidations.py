from typing import List, Optional

from mev_inspect.classifiers.specs import get_classifier
from mev_inspect.schemas.classifiers import LiquidationClassifier
from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.traces import Classification, ClassifiedTrace, DecodedCallTrace
from mev_inspect.schemas.transfers import Transfer
from mev_inspect.traces import get_child_traces, is_child_trace_address
from mev_inspect.transfers import get_child_transfers


def has_liquidations(classified_traces: List[ClassifiedTrace]) -> bool:
    liquidations_exist = False
    for classified_trace in classified_traces:
        if classified_trace.classification == Classification.liquidate:
            liquidations_exist = True
    return liquidations_exist


def get_liquidations(classified_traces: List[ClassifiedTrace]) -> List[Liquidation]:

    liquidations: List[Liquidation] = []
    parent_liquidations: List[DecodedCallTrace] = []

    for trace in classified_traces:

        if not isinstance(trace, DecodedCallTrace):
            continue

        if _is_child_liquidation(trace, parent_liquidations):
            continue

        if trace.classification == Classification.liquidate:

            parent_liquidations.append(trace)
            child_traces = get_child_traces(
                trace.transaction_hash, trace.trace_address, classified_traces
            )
            child_transfers = get_child_transfers(
                trace.transaction_hash, trace.trace_address, child_traces
            )
            liquidation = _parse_liquidation(trace, child_traces, child_transfers)

            if liquidation is not None:
                liquidations.append(liquidation)

    return liquidations


def _parse_liquidation(
    trace: DecodedCallTrace,
    child_traces: List[ClassifiedTrace],
    child_transfers: List[Transfer],
) -> Optional[Liquidation]:

    classifier = get_classifier(trace)

    if classifier is not None and issubclass(classifier, LiquidationClassifier):
        return classifier.parse_liquidation(trace, child_transfers, child_traces)
    return None


def _is_child_liquidation(
    trace: DecodedCallTrace, parent_liquidations: List[DecodedCallTrace]
) -> bool:

    for parent in parent_liquidations:
        if (
            trace.transaction_hash == parent.transaction_hash
            and is_child_trace_address(trace.trace_address, parent.trace_address)
        ):
            return True

    return False
