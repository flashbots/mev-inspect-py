from mev_inspect.schemas.traces import (
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
)


OPEN_SEA_SPEC = [
    ClassifierSpec(
        abi_name="OpenSea",
        protocol=Protocol.opensea,
        valid_contract_addresses=["0x7be8076f4ea4a4ad08075c2508e481d6c946d12b"],
    )
]

OPENSEA_CLASSIFIER_SPECS = [OPEN_SEA_SPEC]
