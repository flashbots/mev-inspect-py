from typing import Optional

from mev_inspect.schemas.classifier_specs import ClassifierSpec
from mev_inspect.schemas.classified_traces import (
    Classification,
    DecodedCallTrace,
)
from mev_inspect.schemas.transfers import ERC20Transfer


def classify_transfer(trace: DecodedCallTrace) -> Optional[ERC20Transfer]:
    return ERC20Transfer(
        block_number=trace.block_number,
        transaction_hash=trace.transaction_hash,
        trace_address=trace.trace_address,
        amount=trace.inputs["amount"],
        to_address=trace.inputs["recipient"],
        from_address=trace.inputs.get("sender", trace.from_address),
        token_address=trace.to_address,
    )


ERC20_SPEC = ClassifierSpec(
    abi_name="ERC20",
    transfer_classifiers={
        "transferFrom(address,address,uint256)": classify_transfer,
        "transfer(address,uint256)": classify_transfer,
    },
    classifications={
        "transferFrom(address,address,uint256)": Classification.transfer,
        "transfer(address,uint256)": Classification.transfer,
    },
)

ERC20_CLASSIFIER_SPECS = [ERC20_SPEC]
