from typing import Optional

from mev_inspect.schemas.classifier_specs import ClassifierSpec
from mev_inspect.schemas.classified_traces import (
    Classification,
    DecodedCallTrace,
    Protocol,
)
from mev_inspect.schemas.transfers import ERC20Transfer


def classify_transfer(trace: DecodedCallTrace) -> Optional[ERC20Transfer]:
    return ERC20Transfer(
        block_number=trace.block_number,
        transaction_hash=trace.transaction_hash,
        trace_address=trace.trace_address,
        amount=trace.inputs["wad"],
        to_address=trace.inputs["dst"],
        from_address=trace.from_address,
        token_address=trace.to_address,
    )


WETH_SPEC = ClassifierSpec(
    abi_name="WETH9",
    protocol=Protocol.weth,
    valid_contract_addresses=["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"],
    transfer_classifiers={
        "transferFrom(address,address,uint256)": classify_transfer,
        "transfer(address,uint256)": classify_transfer,
    },
    classifications={
        "transferFrom(address,address,uint256)": Classification.transfer,
        "transfer(address,uint256)": Classification.transfer,
    },
)


WETH_CLASSIFIER_SPECS = [WETH_SPEC]
