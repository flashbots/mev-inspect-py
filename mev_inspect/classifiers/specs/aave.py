from typing import List, Optional

from mev_inspect.classifiers.helpers import get_debt_transfer, get_received_transfer
from mev_inspect.schemas.classifiers import (
    ClassifiedTrace,
    ClassifierSpec,
    DecodedCallTrace,
    LiquidationClassifier,
    TransferClassifier,
)
from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.traces import Protocol
from mev_inspect.schemas.transfers import Transfer


class AaveLiquidationClassifier(LiquidationClassifier):
    @staticmethod
    def parse_liquidation(
        liquidation_trace: DecodedCallTrace,
        child_transfers: List[Transfer],
        child_traces: List[ClassifiedTrace],
    ) -> Optional[Liquidation]:

        liquidator = liquidation_trace.from_address
        liquidated = liquidation_trace.inputs["_user"]

        debt_token_address = liquidation_trace.inputs["_reserve"]
        received_token_address = liquidation_trace.inputs["_collateral"]

        debt_purchase_amount = None
        received_amount = None

        debt_transfer = get_debt_transfer(liquidator, child_transfers)

        received_transfer = get_received_transfer(liquidator, child_transfers)

        if debt_transfer is not None and received_transfer is not None:

            debt_token_address = debt_transfer.token_address
            debt_purchase_amount = debt_transfer.amount

            received_token_address = received_transfer.token_address
            received_amount = received_transfer.amount

            return Liquidation(
                liquidated_user=liquidated,
                debt_token_address=debt_token_address,
                liquidator_user=liquidator,
                debt_purchase_amount=debt_purchase_amount,
                protocol=Protocol.aave,
                received_amount=received_amount,
                received_token_address=received_token_address,
                transaction_hash=liquidation_trace.transaction_hash,
                trace_address=liquidation_trace.trace_address,
                block_number=liquidation_trace.block_number,
                error=liquidation_trace.error,
            )

        else:
            return None


class AaveTransferClassifier(TransferClassifier):
    @staticmethod
    def get_transfer(trace: DecodedCallTrace) -> Transfer:
        return Transfer(
            block_number=trace.block_number,
            transaction_hash=trace.transaction_hash,
            trace_address=trace.trace_address,
            amount=trace.inputs["value"],
            to_address=trace.inputs["to"],
            from_address=trace.inputs["from"],
            token_address=trace.to_address,
        )


AAVE_SPEC = ClassifierSpec(
    abi_name="AaveLendingPool",
    protocol=Protocol.aave,
    classifiers={
        "liquidationCall(address,address,address,uint256,bool)": AaveLiquidationClassifier,
    },
)

ATOKENS_SPEC = ClassifierSpec(
    abi_name="aTokens",
    protocol=Protocol.aave,
    classifiers={
        "transferOnLiquidation(address,address,uint256)": AaveTransferClassifier,
    },
)

AAVE_CLASSIFIER_SPECS: List[ClassifierSpec] = [AAVE_SPEC, ATOKENS_SPEC]
