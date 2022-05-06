from typing import List, Optional

from mev_inspect.classifiers.helpers import get_debt_transfer, get_received_transfer
from mev_inspect.schemas.classifiers import (
    Classification,
    ClassifiedTrace,
    ClassifierSpec,
    DecodedCallTrace,
    LiquidationClassifier,
    SeizeClassifier,
)
from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.prices import ETH_TOKEN_ADDRESS
from mev_inspect.schemas.traces import Protocol
from mev_inspect.schemas.transfers import Transfer

CYETH_TOKEN_ADDRESS = "0x41c84c0e2ee0b740cf0d31f63f3b6f627dc6b393"


class IronBankLiquidationClassifier(LiquidationClassifier):
    @staticmethod
    def parse_liquidation(
        liquidation_trace: DecodedCallTrace,
        child_transfers: List[Transfer],
        child_traces: List[ClassifiedTrace],
    ) -> Optional[Liquidation]:

        liquidator = liquidation_trace.from_address
        liquidated = liquidation_trace.inputs["borrower"]

        debt_token_address = liquidation_trace.to_address
        received_token_address = liquidation_trace.inputs["cTokenCollateral"]

        debt_purchase_amount = None
        received_amount = None

        debt_purchase_amount, debt_token_address = (
            (liquidation_trace.value, ETH_TOKEN_ADDRESS)
            if debt_token_address == CYETH_TOKEN_ADDRESS
            and liquidation_trace.value != 0
            else (liquidation_trace.inputs["repayAmount"], CYETH_TOKEN_ADDRESS)
        )

        debt_transfer = get_debt_transfer(liquidator, child_transfers)

        received_transfer = get_received_transfer(liquidator, child_transfers)

        seize_trace = _get_seize_call(child_traces)

        if debt_transfer is not None:
            debt_token_address = debt_transfer.token_address
            debt_purchase_amount = debt_transfer.amount

        if received_transfer is not None:
            received_token_address = received_transfer.token_address
            received_amount = received_transfer.amount

        elif seize_trace is not None and seize_trace.inputs is not None:
            received_amount = seize_trace.inputs["seizeTokens"]

        if received_amount is None:
            return None

        return Liquidation(
            liquidated_user=liquidated,
            debt_token_address=debt_token_address,
            liquidator_user=liquidator,
            debt_purchase_amount=debt_purchase_amount,
            protocol=liquidation_trace.protocol,
            received_amount=received_amount,
            received_token_address=received_token_address,
            transaction_hash=liquidation_trace.transaction_hash,
            trace_address=liquidation_trace.trace_address,
            block_number=liquidation_trace.block_number,
            error=liquidation_trace.error,
        )

        return None


IRONBANK_CYETH_SPEC = ClassifierSpec(
    abi_name="CEther",
    protocol=Protocol.ironbank,
    valid_contract_addresses=["0x41c84c0e2EE0b740Cf0d31F63f3B6F627DC6b393"],
    classifiers={
        "liquidateBorrow(address,address)": IronBankLiquidationClassifier,
        "seize(address,address,uint256)": SeizeClassifier,
    },
)

IRONBANK_CTOKEN_SPEC = ClassifierSpec(
    abi_name="CToken",
    protocol=Protocol.ironbank,
    valid_contract_addresses=[
        "0x41c84c0e2ee0b740cf0d31f63f3b6f627dc6b393",  # cyWETH
        "0x8e595470ed749b85c6f7669de83eae304c2ec68f",  # cyDAI
        "0xe7bff2da8a2f619c2586fb83938fa56ce803aa16",  # cyLINK
        "0xfa3472f7319477c9bfecdd66e4b948569e7621b9",  # cyYFI
        "0x12a9cc33a980daa74e00cc2d1a0e74c57a93d12c",  # cySNX
        "0x8fc8bfd80d6a9f17fb98a373023d72531792b431",  # cyWBTC
        "0x48759f220ed983db51fa7a8c0d2aab8f3ce4166a",  # cyUSDT
        "0x76eb2fe28b36b3ee97f3adae0c69606eedb2a37c",  # cyUDSC
        "0xa7c4054afd3dbbbf5bfe80f41862b89ea05c9806",  # cySUSD
        "0xa8caea564811af0e92b1e044f3edd18fa9a73e4f",  # cyEURS
        "0xca55f9c4e77f7b8524178583b0f7c798de17fd54",  # cySEUR
        "0x7736ffb07104c0c400bb0cc9a7c228452a732992",  # cyDPI
        "0xbddeb563e90f6cbf168a7cda4927806477e5b6c6",  # cyUSDP
        "0xFEEB92386A055E2eF7C2B598c872a4047a7dB59F",  # cyUNI
        "0x226F3738238932BA0dB2319a8117D9555446102f",  # cySUSHI
        "0xB8c5af54bbDCc61453144CF472A9276aE36109F9",  # cyCRV
        "0x30190a3B52b5AB1daF70D46D72536F5171f22340",  # cyAAVE
        "0x9e8E207083ffd5BDc3D99A1F32D1e6250869C1A9",  # iMIM
        "0xE0B57FEEd45e7D908f2d0DaCd26F113Cf26715BF",  # iCVX
        "0xd2b0D3594427e0c57C39e3455E2FB2dFED1e0B99",  # iAPE
    ],
    classifiers={
        "liquidateBorrow(address,uint256,address)": IronBankLiquidationClassifier,
        "seize(address,address,uint256)": SeizeClassifier,
    },
)

IRONBANK_CLASSIFIER_SPECS: List[ClassifierSpec] = [
    IRONBANK_CYETH_SPEC,
    IRONBANK_CTOKEN_SPEC,
]


def _get_seize_call(traces: List[ClassifiedTrace]) -> Optional[ClassifiedTrace]:
    """Find the call to `seize` in the child traces (successful liquidation)"""
    for trace in traces:
        if trace.classification == Classification.seize:
            return trace
    return None
