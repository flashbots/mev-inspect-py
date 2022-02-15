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
from mev_inspect.schemas.prices import CETH_TOKEN_ADDRESS, ETH_TOKEN_ADDRESS
from mev_inspect.schemas.traces import Protocol
from mev_inspect.schemas.transfers import Transfer


class CompoundLiquidationClassifier(LiquidationClassifier):
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
            if debt_token_address == CETH_TOKEN_ADDRESS and liquidation_trace.value != 0
            else (liquidation_trace.inputs["repayAmount"], CETH_TOKEN_ADDRESS)
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


COMPOUND_V2_CETH_SPEC = ClassifierSpec(
    abi_name="CEther",
    protocol=Protocol.compound_v2,
    valid_contract_addresses=["0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5"],
    classifiers={
        "liquidateBorrow(address,address)": CompoundLiquidationClassifier,
        "seize(address,address,uint256)": SeizeClassifier,
    },
)

COMPOUND_V2_CTOKEN_SPEC = ClassifierSpec(
    abi_name="CToken",
    protocol=Protocol.compound_v2,
    valid_contract_addresses=[
        "0x6c8c6b02e7b2be14d4fa6022dfd6d75921d90e4e",
        "0x5d3a536e4d6dbd6114cc1ead35777bab948e3643",
        "0x158079ee67fce2f58472a96584a73c7ab9ac95c1",
        "0x39aa39c021dfbae8fac545936693ac917d5e7563",
        "0xf650c3d88d12db855b8bf7d11be6c55a4e07dcc9",
        "0xc11b1268c1a384e55c48c2391d8d480264a3a7f4",
        "0xb3319f5d18bc0d84dd1b4825dcde5d5f7266d407",
        "0xf5dce57282a584d2746faf1593d3121fcac444dc",
        "0x35a18000230da775cac24873d00ff85bccded550",
        "0x70e36f6bf80a52b3b46b3af8e106cc0ed743e8e4",
        "0xccf4429db6322d5c611ee964527d42e5d685dd6a",
        "0x12392f67bdf24fae0af363c24ac620a2f67dad86",
        "0xface851a4921ce59e912d19329929ce6da6eb0c7",
        "0x95b4ef2869ebd94beb4eee400a99824bf5dc325b",
        "0x4b0181102a0112a2ef11abee5563bb4a3176c9d7",
        "0xe65cdb6479bac1e22340e4e755fae7e509ecd06c",
        "0x80a2ae356fc9ef4305676f7a3e2ed04e12c33946",
    ],
    classifiers={
        "liquidateBorrow(address,uint256,address)": CompoundLiquidationClassifier,
        "seize(address,address,uint256)": SeizeClassifier,
    },
)

COMPOUND_CLASSIFIER_SPECS: List[ClassifierSpec] = [
    COMPOUND_V2_CETH_SPEC,
    COMPOUND_V2_CTOKEN_SPEC,
]


def _get_seize_call(traces: List[ClassifiedTrace]) -> Optional[ClassifiedTrace]:
    """Find the call to `seize` in the child traces (successful liquidation)"""
    for trace in traces:
        if trace.classification == Classification.seize:
            return trace
    return None
