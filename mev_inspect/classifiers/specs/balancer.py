from typing import Optional, List
from mev_inspect.schemas.transfers import Transfer
from mev_inspect.schemas.swaps import Swap
from mev_inspect.schemas.traces import (
    DecodedCallTrace,
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    SwapClassifier,
)
from mev_inspect.classifiers.helpers import create_swap_from_pool_transfers

BALANCER_V1_POOL_ABI_NAME = "BPool"


class BalancerSwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        trace: DecodedCallTrace,
        prior_transfers: List[Transfer],
        child_transfers: List[Transfer],
    ) -> Optional[Swap]:

        recipient_address = trace.from_address

        swap = create_swap_from_pool_transfers(
            trace, recipient_address, prior_transfers, child_transfers
        )
        return swap


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
