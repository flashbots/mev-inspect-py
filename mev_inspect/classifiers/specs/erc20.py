from mev_inspect.schemas.classified_traces import (
    Classification,
    ClassifierSpec,
)


ERC20_SPEC = ClassifierSpec(
    abi_name="ERC20",
    classifications={
        "transferFrom(address,address,uint256)": Classification.transfer,
        "transfer(address,uint256)": Classification.transfer,
        "burn(address)": Classification.burn,
    },
)

ERC20_CLASSIFIER_SPECS = [ERC20_SPEC]
