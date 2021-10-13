from mev_inspect.schemas.classified_traces import (
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    LiquidationClassifier,
    SeizeClassifier,
)

COMPOUND_V2_CETH_SPEC = ClassifierSpec(
    abi_name="CEther",
    protocol=Protocol.compound_v2,
    classifiers={
        "liquidateBorrow(address,address)": LiquidationClassifier,
        "seize(address,address,uint256)": SeizeClassifier,
    },
)

COMPOUND_V2_CTOKEN_SPEC = ClassifierSpec(
    abi_name="CToken",
    protocol=Protocol.compound_v2,
    classifiers={
        "liquidateBorrow(address,uint256,address)": LiquidationClassifier,
        "seize(address,address,uint256)": SeizeClassifier,
    },
)

COMPOUND_CLASSIFIER_SPECS = [COMPOUND_V2_CETH_SPEC, COMPOUND_V2_CTOKEN_SPEC]
