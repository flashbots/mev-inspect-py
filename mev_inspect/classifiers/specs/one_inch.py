from typing import List, Optional

from mev_inspect.schemas.classifiers import ClassifierSpec, SwapClassifier
from mev_inspect.schemas.swaps import Swap
from mev_inspect.schemas.traces import DecodedCallTrace, Protocol
from mev_inspect.schemas.transfers import Transfer


class OneInchSwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        trace: DecodedCallTrace,
        prior_transfers: List[Transfer],
        child_transfers: List[Transfer],
    ) -> Optional[Swap]:
        if trace.error is not None:
            return None

        desc = trace.inputs["desc"]
        [srcToken, dstToken, srcReceiver, dstReceiver, amountIn, *_] = desc

        transfer_out_candidates = [
            transfer
            for transfer in child_transfers
            if (
                transfer.token_address == dstToken
                and transfer.to_address == dstReceiver
            )
        ]

        if len(transfer_out_candidates) == 0:
            raise RuntimeError("1inch expected at least one transfer out")

        return Swap(
            abi_name=trace.abi_name,
            transaction_hash=trace.transaction_hash,
            transaction_position=trace.transaction_position,
            block_number=trace.block_number,
            trace_address=trace.trace_address,
            contract_address=trace.to_address,
            protocol=trace.protocol,
            from_address=srcReceiver,
            to_address=dstReceiver,
            token_in_address=srcToken,
            token_in_amount=amountIn,
            token_out_address=dstToken,
            token_out_amount=transfer_out_candidates[0].amount,
            error=trace.error,
        )


ONE_INCH_ROUTER_SPEC = ClassifierSpec(
    abi_name="AggregationRouterV3",
    protocol=Protocol.one_inch,
    classifiers={
        "swap(address,(address,address,address,address,uint256,uint256,uint256,bytes),bytes)": OneInchSwapClassifier,
    },
)

ONE_INCH_CLASSIFIER_SPECS = [ONE_INCH_ROUTER_SPEC]
