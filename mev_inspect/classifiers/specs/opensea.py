from typing import List
from mev_inspect.classifiers.helpers import _filter_transfers
from mev_inspect.schemas.classifiers import ClassifierSpec, NftTradeClassifier
from mev_inspect.schemas.nft_trade import NftTrade
from mev_inspect.schemas.traces import DecodedCallTrace, Protocol
from mev_inspect.schemas.transfers import ETH_TOKEN_ADDRESS, Transfer

OPENSEA_ETH_TOKEN_ADDRESS = "0x0000000000000000000000000000000000000000"

class OpenseaClassifier(NftTradeClassifier):    
    @staticmethod
    def parse_trade(trace: DecodedCallTrace) -> NftTrade:
        uints = trace.inputs.get("uints")
        addresses = trace.inputs.get("addrs")
        buy_maker = addresses[1]
        sell_maker = addresses[8]
        base_price = uints[4]
        payment_token = addresses[6]
        target = addresses[4]

        if payment_token == OPENSEA_ETH_TOKEN_ADDRESS:
            # Opensea uses the zero-address as a sentinel value for Ether. Convert this
            # to the normal eth token address.
            payment_token = ETH_TOKEN_ADDRESS

        return NftTrade(
            abi_name=trace.abi_name,
            transaction_hash=trace.transaction_hash,
            transaction_position=trace.transaction_position,
            block_number=trace.block_number,
            trace_address=trace.trace_address,
            protocol=trace.protocol,
            error=trace.error,
            seller_address=sell_maker,
            buyer_address=buy_maker,
            payment_token=payment_token,
            payment_amount=base_price,
            collection_address=target,
            token_uri=0 # Todo
        )


OPENSEA_SPEC= ClassifierSpec(
    abi_name="WyvernExchange",
    protocol=Protocol.opensea,
    valid_contract_addresses=["0x7be8076f4ea4a4ad08075c2508e481d6c946d12b"],
    classifiers={
        "atomicMatch_(address[14],uint256[18],uint8[8],bytes,bytes,bytes,bytes,bytes,bytes,uint8[2],bytes32[5])": OpenseaClassifier, # TODO actual types
    },
)

OPENSEA_CLASSIFIER_SPECS = [OPENSEA_SPEC]
