from typing import List, Optional
from mev_inspect.classifiers.specs import get_classifier
from mev_inspect.schemas.classifiers import NftTradeClassifier
from mev_inspect.schemas.nft_trade import NftTrade
from mev_inspect.schemas.traces import Classification, ClassifiedTrace, DecodedCallTrace
from mev_inspect.schemas.transfers import Transfer
from mev_inspect.traces import get_traces_by_transaction_hash

def get_nft_trades(traces: List[ClassifiedTrace]) -> List[NftTrade]:
    nft_trades = []

    for _, transaction_traces in get_traces_by_transaction_hash(traces).items():
        nft_trades += _get_nft_trades_for_transaction(
            list(transaction_traces)
        )

    return nft_trades


def _get_nft_trades_for_transaction(
    traces: List[ClassifiedTrace],
) -> List[NftTrade]:
    ordered_traces = list(sorted(traces, key=lambda t: t.trace_address))

    nft_trades: List[NftTrade] = []

    for trace in ordered_traces:
        if not isinstance(trace, DecodedCallTrace):
            continue

        elif trace.classification == Classification.nft_trade:
            nft_transfer = _parse_trade(trace)

            nft_trades.append(nft_transfer)

    return nft_trades

def _parse_trade(trace: DecodedCallTrace) -> Optional[NftTrade]:
    classifier = get_classifier(trace)

    if classifier is not None and issubclass(classifier, NftTradeClassifier):
        return classifier.parse_trade(trace)

    return None
