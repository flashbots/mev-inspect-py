from mev_inspect.schemas.classified_traces import (
    Classification,
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    Classifier,
)


BALANCER_V1_SPECS = [
    ClassifierSpec(
        abi_name="BPool",
        protocol=Protocol.balancer_v1,
        classifiers={
            "swapExactAmountIn(address,uint256,address,uint256,uint256)": Classifier(
                classification=Classification.swap,
            ),
            "swapExactAmountOut(address,uint256,address,uint256,uint256)": Classifier(
                classification=Classification.swap,
            ),
        },
    ),
]

BALANCER_CLASSIFIER_SPECS = [
    *BALANCER_V1_SPECS,
]
