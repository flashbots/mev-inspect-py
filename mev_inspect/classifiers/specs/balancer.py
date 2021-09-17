from mev_inspect.schemas.classified_traces import (
    Classification,
    ClassifierSpec,
    Protocol,
)

BALANCER_V1_SPECS = [
    ClassifierSpec(
        abi_name="BPool",
        protocol=Protocol.balancer_v1,
        classifications={
            "swapExactAmountIn(address,uint256,address,uint256,uint256)": Classification.swap,
            "swapExactAmountOut(address,uint256,address,uint256,uint256)": Classification.swap,
        },
    ),
]

BALANCER_CLASSIFIER_SPECS = [
    *BALANCER_V1_SPECS,
]
