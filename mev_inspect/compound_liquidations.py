from typing import Dict, List, Optional
from web3 import Web3

from mev_inspect.traces import get_child_traces
from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    Classification,
    Protocol,
)

from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.classifiers.specs import WETH_ADDRESS
from mev_inspect.abi import get_raw_abi

V2_COMPTROLLER_ADDRESS = "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B"
V2_C_ETHER = "0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5"

# helper, only queried once in the beginning (inspect_block)
def fetch_all_comp_markets(w3: Web3) -> Dict[str, str]:
    c_token_mapping = {}
    comp_v2_comptroller_abi = get_raw_abi("Comptroller", Protocol.compound_v2)
    comptroller_instance = w3.eth.contract(
        address=V2_COMPTROLLER_ADDRESS, abi=comp_v2_comptroller_abi
    )
    markets = comptroller_instance.functions.getAllMarkets().call()
    comp_v2_ctoken_abi = get_raw_abi("CToken", Protocol.compound_v2)
    for c_token in markets:
        # make an exception for cETH (as it has no .underlying())
        if c_token != V2_C_ETHER:
            ctoken_instance = w3.eth.contract(address=c_token, abi=comp_v2_ctoken_abi)
            underlying_token = ctoken_instance.functions.underlying().call()
            c_token_mapping[
                c_token.lower()
            ] = underlying_token.lower()  # make k:v lowercase for consistancy
    return c_token_mapping


def get_compound_liquidations(
    traces: List[ClassifiedTrace], collateral_by_c_token_address: Dict[str, str]
) -> List[Liquidation]:

    """Inspect list of classified traces and identify liquidation"""
    liquidations: List[Liquidation] = []

    for trace in traces:
        if (
            trace.classification == Classification.liquidate
            and trace.protocol == Protocol.compound_v2
            and trace.inputs is not None
            and trace.to_address is not None
        ):
            # First, we look for cEther liquidations (position paid back via tx.value)
            child_traces = get_child_traces(
                trace.transaction_hash, trace.trace_address, traces
            )
            seize_trace = _get_seize_call(child_traces)
            if seize_trace is not None and seize_trace.inputs is not None:
                c_token_collateral = trace.inputs["cTokenCollateral"]
                if trace.abi_name == "CEther":
                    liquidations.append(
                        Liquidation(
                            liquidated_user=trace.inputs["borrower"],
                            collateral_token_address=WETH_ADDRESS,  # WETH since all cEther liquidations provide Ether
                            debt_token_address=c_token_collateral,
                            liquidator_user=seize_trace.inputs["liquidator"],
                            debt_purchase_amount=trace.value,
                            protocol=Protocol.compound_v2,
                            received_amount=seize_trace.inputs["seizeTokens"],
                            transaction_hash=trace.transaction_hash,
                            trace_address=trace.trace_address,
                            block_number=trace.block_number,
                        )
                    )
                elif (
                    trace.abi_name == "CToken"
                ):  # cToken liquidations where liquidator pays back via token transfer
                    c_token_address = trace.to_address
                    liquidations.append(
                        Liquidation(
                            liquidated_user=trace.inputs["borrower"],
                            collateral_token_address=collateral_by_c_token_address[
                                c_token_address
                            ],
                            debt_token_address=c_token_collateral,
                            liquidator_user=seize_trace.inputs["liquidator"],
                            debt_purchase_amount=trace.inputs["repayAmount"],
                            protocol=Protocol.compound_v2,
                            received_amount=seize_trace.inputs["seizeTokens"],
                            transaction_hash=trace.transaction_hash,
                            trace_address=trace.trace_address,
                            block_number=trace.block_number,
                        )
                    )
    return liquidations


def _get_seize_call(traces: List[ClassifiedTrace]) -> Optional[ClassifiedTrace]:
    """Find the call to `seize` in the child traces (successful liquidation)"""
    for trace in traces:
        if trace.classification == Classification.seize:
            return trace
    return None
