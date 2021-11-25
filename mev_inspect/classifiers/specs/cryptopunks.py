from mev_inspect.schemas.traces import Protocol, Classification

from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    Classifier,
)


class PunkBidAcceptanceClassifier(Classifier):
    @staticmethod
    def get_classification() -> Classification:
        return Classification.punk_accept_bid


class PunkBidClassifier(Classifier):
    @staticmethod
    def get_classification() -> Classification:
        return Classification.punk_bid


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
