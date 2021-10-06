from mev_inspect.schemas.classified_traces import (
    Classification,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    Classifier,
)


ERC20_SPEC = ClassifierSpec(
    abi_name="ERC20",
    classifiers={
        "transferFrom(address,address,uint256)": Classifier(
            classification=Classification.transfer,
        ),
        "transfer(address,uint256)": Classifier(
            classification=Classification.transfer,
        ),
    },
)

ERC20_CLASSIFIER_SPECS = [ERC20_SPEC]
