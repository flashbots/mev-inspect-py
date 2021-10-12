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

ATOKENS_SPEC = ClassifierSpec(
    abi_name="aTokens",
    protocol=Protocol.aave,
    classifications={
        "transferOnLiquidation(address,address,uint256)": Classification.transfer,
        "transferFrom(address,address,uint256)": Classification.transfer,
    },
)

AAVE_CLASSIFIER_SPECS = [AAVE_SPEC]
