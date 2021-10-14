from mev_inspect.schemas.classified_traces import (
    DecodedCallTrace,
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    SwapClassifier,
)


BALANCER_V1_POOL_ABI_NAME = "BPool"


class BalancerSwapClassifier(SwapClassifier):
    @staticmethod
    def get_swap_recipient(trace: DecodedCallTrace) -> str:
        return trace.from_address


BALANCER_V1_SPECS = [
    ClassifierSpec(
        abi_name=BALANCER_V1_POOL_ABI_NAME,
        protocol=Protocol.balancer_v1,
        classifiers={
            "swapExactAmountIn(address,uint256,address,uint256,uint256)": BalancerSwapClassifier,
            "swapExactAmountOut(address,uint256,address,uint256,uint256)": BalancerSwapClassifier,
        },
    ),
]

BALANCER_CLASSIFIER_SPECS = [
    *BALANCER_V1_SPECS,
]
