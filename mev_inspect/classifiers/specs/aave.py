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

AAVE_CLASSIFIER_SPECS = [AAVE_SPEC]
