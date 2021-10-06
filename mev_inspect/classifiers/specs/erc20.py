from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    TransferClassifier,
)


ERC20_SPEC = ClassifierSpec(
    abi_name="ERC20",
    classifiers={
        "transferFrom(address,address,uint256)": TransferClassifier(),
        "transfer(address,uint256)": TransferClassifier(),
    },
)

ERC20_CLASSIFIER_SPECS = [ERC20_SPEC]
