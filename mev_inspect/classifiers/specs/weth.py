from mev_inspect.schemas.classified_traces import (
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    DecodedCallTrace,
    TransferClassifier,
)
from mev_inspect.schemas.transfers import ERC20Transfer


def get_weth_transfer(trace: DecodedCallTrace) -> ERC20Transfer:
    return ERC20Transfer(
        block_number=trace.block_number,
        transaction_hash=trace.transaction_hash,
        trace_address=trace.trace_address,
        amount=trace.inputs["wad"],
        to_address=trace.inputs["dst"],
        from_address=trace.from_address,
        token_address=trace.to_address,
    )


WETH_TRANSFER_CLASSIFIER = TransferClassifier(get_transfer=get_weth_transfer)

WETH_SPEC = ClassifierSpec(
    abi_name="WETH9",
    protocol=Protocol.weth,
    valid_contract_addresses=["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"],
    classifiers={
        "transferFrom(address,address,uint256)": WETH_TRANSFER_CLASSIFIER,
        "transfer(address,uint256)": WETH_TRANSFER_CLASSIFIER,
    },
)

WETH_CLASSIFIER_SPECS = [WETH_SPEC]
