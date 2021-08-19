from mev_inspect.schemas.classified_traces import (
    Classification,
    ClassifierSpec,
    Protocol,
)

AAVE_SPEC = ClassifierSpec(
    abi_name="AaveLendingPool",
    protocol=Protocol.aave,
    classifications={
        "liquidationCall(address,address,address,uint256,bool)": Classification.liquidate,
    },
)

AAVE_CLASSIFIER_SPECS = [AAVE_SPEC]
