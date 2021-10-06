from mev_inspect.schemas.classified_traces import (
    Classification,
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    Classifier,
)


AAVE_SPEC = ClassifierSpec(
    abi_name="AaveLendingPool",
    protocol=Protocol.aave,
    classifiers={
        "liquidationCall(address,address,address,uint256,bool)": Classifier(
            classification=Classification.liquidate,
        )
    },
)

AAVE_CLASSIFIER_SPECS = [AAVE_SPEC]
