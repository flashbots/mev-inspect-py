from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    DecodedCallTrace,
    TransferClassifier,
    LiquidationClassifier,
)
from mev_inspect.schemas.traces import Protocol
from mev_inspect.schemas.transfers import Transfer


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
        "liquidationCall(address,address,address,uint256,bool)": LiquidationClassifier,
    },
)

ATOKENS_SPEC = ClassifierSpec(
    abi_name="aTokens",
    protocol=Protocol.aave,
    classifiers={
        "transferOnLiquidation(address,address,uint256)": AaveTransferClassifier,
        "transferFrom(address,address,uint256)": AaveTransferClassifier,
    },
)

AAVE_CLASSIFIER_SPECS = [AAVE_SPEC, ATOKENS_SPEC]
