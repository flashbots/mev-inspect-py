from typing import List, Optional, Tuple

from mev_inspect.schemas.classifiers import (
    Classifier,
    ClassifierSpec,
    DecodedCallTrace,
    TransferClassifier,
)
from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.traces import Protocol
from mev_inspect.schemas.transfers import Transfer


class AaveLiquidationClassifier(Classifier):
    def parse_liquidation(
        self, liquidation_trace: DecodedCallTrace, child_transfers: List[Transfer]
    ) -> Optional[Liquidation]:

        liquidator = liquidation_trace.from_address

        (debt_token_address, debt_purchase_amount) = self._get_debt_data(
            liquidation_trace, child_transfers, liquidator
        )

        if debt_purchase_amount == 0:
            return None

        (received_token_address, received_amount) = self._get_received_data(
            liquidation_trace, child_transfers, liquidator
        )

        if received_amount == 0:
            return None

        return Liquidation(
            liquidated_user=liquidation_trace.inputs["_user"],
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

    def _get_received_data(
        self,
        liquidation_trace: DecodedCallTrace,
        child_transfers: List[Transfer],
        liquidator: str,
    ) -> Tuple[str, int]:

        """Look for and return liquidator payback from liquidation"""
        for transfer in child_transfers:

            if transfer.to_address == liquidator:
                return transfer.token_address, transfer.amount

        return liquidation_trace.inputs["_collateral"], 0

    def _get_debt_data(
        self,
        liquidation_trace: DecodedCallTrace,
        child_transfers: List[Transfer],
        liquidator: str,
    ) -> Tuple[str, int]:
        """Get transfer from liquidator to AAVE"""

        for transfer in child_transfers:
            if transfer.from_address == liquidator:
                return transfer.token_address, transfer.amount

        return liquidation_trace.inputs["_reserve"], 0


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
