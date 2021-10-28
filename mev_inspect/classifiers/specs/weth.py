from mev_inspect.schemas.traces import (
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    DecodedCallTrace,
    TransferClassifier,
)
from mev_inspect.schemas.transfers import Transfer


class WethTransferClassifier(TransferClassifier):
    @staticmethod
    def get_transfer(trace: DecodedCallTrace) -> Transfer:
        return Transfer(
            block_number=trace.block_number,
            transaction_hash=trace.transaction_hash,
            trace_address=trace.trace_address,
            amount=trace.inputs["wad"],
            to_address=trace.inputs["dst"],
            from_address=trace.from_address,
            token_address=trace.to_address,
        )


WETH_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

WETH_SPEC = ClassifierSpec(
    abi_name="WETH9",
    protocol=Protocol.weth,
    valid_contract_addresses=[WETH_ADDRESS],
    classifiers={
        "transferFrom(address,address,uint256)": WethTransferClassifier,
        "transfer(address,uint256)": WethTransferClassifier,
    },
)

WETH_CLASSIFIER_SPECS = [WETH_SPEC]
