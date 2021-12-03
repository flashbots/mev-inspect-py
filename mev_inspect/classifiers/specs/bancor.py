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
from mev_inspect.classifiers.helpers import (
    create_swap_from_recipient_transfers,
)

BANCOR_NETWORK_ABI_NAME = "BancorNetwork"
BANCOR_NETWORK_CONTRACT_ADDRESS = "0x2F9EC37d6CcFFf1caB21733BdaDEdE11c823cCB0"


class BancorSwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        trace: DecodedCallTrace,
        prior_transfers: List[Transfer],
        child_transfers: List[Transfer],
    ) -> Optional[Swap]:
        recipient_address = trace.from_address

        swap = create_swap_from_recipient_transfers(
            trace,
            BANCOR_NETWORK_CONTRACT_ADDRESS,
            recipient_address,
            prior_transfers,
            child_transfers,
        )
        return swap


BANCOR_NETWORK_SPEC = ClassifierSpec(
    abi_name=BANCOR_NETWORK_ABI_NAME,
    protocol=Protocol.bancor,
    classifiers={
        "convertByPath(address[],uint256,uint256,address,address,uint256)": BancorSwapClassifier,
    },
    valid_contract_addresses=[BANCOR_NETWORK_CONTRACT_ADDRESS],
)

BANCOR_CLASSIFIER_SPECS = [BANCOR_NETWORK_SPEC]
