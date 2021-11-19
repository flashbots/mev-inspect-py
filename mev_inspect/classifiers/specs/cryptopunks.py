from mev_inspect.schemas.traces import (
    Protocol,
)

from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    PunkBidClassifier,
    PunkBidAcceptanceClassifier,
)

CRYPTO_PUNKS_SPEC = ClassifierSpec(
    abi_name="cryptopunks",
    protocol=Protocol.cryptopunks,
    valid_contract_addresses=["0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB"],
    classifiers={
        "enterBidForPunk(uint256)": PunkBidClassifier,
        "acceptBidForPunk(uint256,uint256)": PunkBidAcceptanceClassifier,
    },
)

CRYPTOPUNKS_CLASSIFIER_SPECS = [CRYPTO_PUNKS_SPEC]
