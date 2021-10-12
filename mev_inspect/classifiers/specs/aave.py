from mev_inspect.schemas.classified_traces import (
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    LiquidationClassifier,
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
    classifications={
        "transferOnLiquidation(address,address,uint256)": Classification.transfer,
        "transferFrom(address,address,uint256)": Classification.transfer,
    },
)

AAVE_CLASSIFIER_SPECS = [AAVE_SPEC]
