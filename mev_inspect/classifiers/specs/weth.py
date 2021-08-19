from mev_inspect.schemas.classified_traces import (
    Classification,
    ClassifierSpec,
    Protocol,
)

WETH_SPEC = ClassifierSpec(
    abi_name="WETH9",
    protocol=Protocol.weth,
    valid_contract_addresses=["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"],
    classifications={
        "transferFrom(address,address,uint256)": Classification.transfer,
        "transfer(address,uint256)": Classification.transfer,
    },
)

WETH_CLASSIFIER_SPECS = [WETH_SPEC]
