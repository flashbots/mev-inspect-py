from mev_inspect.schemas.classified_traces import (
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    SwapClassifier,
)


BALANCER_V1_SPECS = [
    ClassifierSpec(
        abi_name="BPool",
        protocol=Protocol.balancer_v1,
        classifiers={
            "swapExactAmountIn(address,uint256,address,uint256,uint256)": SwapClassifier(),
            "swapExactAmountOut(address,uint256,address,uint256,uint256)": SwapClassifier(),
        },
    ),
]

BALANCER_CLASSIFIER_SPECS = [
    *BALANCER_V1_SPECS,
]
