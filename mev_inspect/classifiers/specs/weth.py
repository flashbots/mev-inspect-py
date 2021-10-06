from mev_inspect.schemas.classified_traces import (
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    TransferClassifier,
)


WETH_SPEC = ClassifierSpec(
    abi_name="WETH9",
    protocol=Protocol.weth,
    valid_contract_addresses=["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"],
    classifiers={
        "transferFrom(address,address,uint256)": TransferClassifier(),
        "transfer(address,uint256)": TransferClassifier(),
    },
)

WETH_CLASSIFIER_SPECS = [WETH_SPEC]
