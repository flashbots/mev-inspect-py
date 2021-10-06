from mev_inspect.schemas.classified_traces import (
    Classification,
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    Classifier,
)


WETH_SPEC = ClassifierSpec(
    abi_name="WETH9",
    protocol=Protocol.weth,
    valid_contract_addresses=["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"],
    classifiers={
        "transferFrom(address,address,uint256)": Classifier(
            classification=Classification.transfer,
        ),
        "transfer(address,uint256)": Classifier(
            classification=Classification.transfer,
        ),
    },
)

WETH_CLASSIFIER_SPECS = [WETH_SPEC]
