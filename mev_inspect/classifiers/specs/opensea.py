from mev_inspect.schemas.classified_traces import (
    DecodedCallTrace,
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    AtomicMatchClassifier,
)

OPENSEA_ATOMIC_MATCH_ABI_NAME='atomicMatch_'

OPENSEA_SPEC = [
    ClassifierSpec(
        abi_name="atomicMatch_",
        protocol=Protocol.opensea,
        valid_contract_addresses=["0x7be8076f4ea4a4ad08075c2508e481d6c946d12b"],
    ),
]
