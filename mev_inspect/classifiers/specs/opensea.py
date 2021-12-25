from typing import List, Optional

from mev_inspect.classifiers.helpers import create_nft_trade_from_transfers
from mev_inspect.schemas.classifiers import ClassifierSpec, NftTradeClassifier
from mev_inspect.schemas.nft_trades import NftTrade
from mev_inspect.schemas.traces import DecodedCallTrace, Protocol
from mev_inspect.schemas.transfers import Transfer

OPENSEA_WALLET_ADDRESS = "0x5b3256965e7c3cf26e11fcaf296dfc8807c01073"


class OpenseaClassifier(NftTradeClassifier):
    @staticmethod
    def parse_trade(
        trace: DecodedCallTrace,
        child_transfers: List[Transfer],
    ) -> Optional[NftTrade]:
        addresses = trace.inputs["addrs"]
        buy_maker = addresses[1]
        sell_maker = addresses[8]
        target = addresses[4]

        return create_nft_trade_from_transfers(
            trace,
            child_transfers,
            collection_address=target,
            seller_address=sell_maker,
            buyer_address=buy_maker,
            exchange_wallet_address=OPENSEA_WALLET_ADDRESS,
        )


OPENSEA_SPEC = ClassifierSpec(
    abi_name="WyvernExchange",
    protocol=Protocol.opensea,
    valid_contract_addresses=["0x7be8076f4ea4a4ad08075c2508e481d6c946d12b"],
    classifiers={
        "atomicMatch_(address[14],uint256[18],uint8[8],bytes,bytes,bytes,bytes,bytes,bytes,uint8[2],bytes32[5])": OpenseaClassifier,
    },
)

OPENSEA_CLASSIFIER_SPECS = [OPENSEA_SPEC]
