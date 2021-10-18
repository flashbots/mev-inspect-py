from mev_inspect.schemas.classified_traces import (
    DecodedCallTrace,
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    SwapClassifier,
)


class OneInchFillOrderProtocolSwapClassifier(SwapClassifier):
    @staticmethod
    def get_swap_recipient(trace: DecodedCallTrace) -> str:
        return trace.from_address


FILL_ORDER_SIGNATURE = (
    "fillOrder((uint256,address,address,bytes,bytes,bytes,bytes,bytes,bytes,bytes),"
    "bytes,uint256,uint256,uint256)"
)


FILL_ORDER_SIGNATURE = (
    "fillOrder((uint256,address,address,bytes,bytes,bytes,bytes,bytes,bytes,bytes),"
    "bytes,uint256,uint256,uint256)"
)

ONE_INCH_LIMIT_ORDER_PROTOCOL_SPEC = ClassifierSpec(
    abi_name="1inchLimitOrderProtocol",
    protocol=Protocol.one_inch,
    classifications={
        FILL_ORDER_SIGNATURE: OneInchFillOrderProtocolSwapClassifier,
    },
)

ONE_INCH_CLASSIFIER_SPECS = [ONE_INCH_LIMIT_ORDER_PROTOCOL_SPEC]
