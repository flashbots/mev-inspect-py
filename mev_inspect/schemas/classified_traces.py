from enum import Enum

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .blocks import Trace

from .utils import CamelModel

# -------- Enums ------------------------------------------------------------------------------


class Classification(Enum):
    unknown = "unknown"
    swap = "swap"
    burn = "burn"
    transfer = "transfer"
    liquidate = "liquidate"


class Protocol(Enum):
    uniswap_v2 = "uniswap_v2"
    uniswap_v3 = "uniswap_v3"
    sushiswap = "sushiswap"
    aave = "aave"
    weth = "weth"
    curve = "curve"


# -------- Trace Models ------------------------------------------------------------------------------


class ClassifiedTrace(Trace):

    transaction_hash: str
    block_number: int
    trace_address: List[int]
    classification: Classification
    error: Optional[str]
    to_address: Optional[str]
    from_address: Optional[str]
    gas: Optional[int]
    value: Optional[int]
    gas_used: Optional[int]
    protocol: Optional[Protocol]
    function_name: Optional[str]
    function_signature: Optional[str]
    inputs: Optional[Dict[str, Any]]
    abi_name: Optional[str]

    class Config:
        json_encoders = {
            # a little lazy but fine for now
            # this is used for bytes value inputs
            bytes: lambda b: b.hex(),
        }


class Call(ClassifiedTrace):

    to_address: str
    from_address: str


class ClassifiedCall(ClassifiedTrace):

    inputs: Dict[str, Any]
    abi_name: str

    gas: Optional[int]
    gas_used: Optional[int]
    function_name: Optional[str]
    function_signature: Optional[str]


# -------- Swaps ------------------------------------------------------------------------------


class Swap(BaseModel):
    abi_name: str
    transaction_hash: str
    block_number: int
    trace_address: List[int]
    protocol: Optional[Protocol]
    pool_address: str
    from_address: str
    to_address: str
    token_in_address: str
    token_in_amount: int
    token_out_address: str
    token_out_amount: int
    error: Optional[str]


class Arbitrage(BaseModel):
    swaps: List[Swap]
    block_number: int
    transaction_hash: str
    account_address: str
    profit_token_address: str
    start_amount: int
    end_amount: int
    profit_amount: int


# -------- Transfers------------------------------------------------------------------------------


class Transfer(BaseModel):
    transaction_hash: str
    trace_address: List[int]
    from_address: str
    to_address: str
    amount: int
    token_address: str

    @classmethod
    def from_trace(cls, trace: ClassifiedTrace) -> "Transfer":
        if trace.classification != Classification.transfer or trace.inputs is None:
            raise ValueError("Invalid transfer")

        if trace.protocol == Protocol.weth:
            return cls(
                transaction_hash=trace.transaction_hash,
                trace_address=trace.trace_address,
                amount=trace.inputs["wad"],
                to_address=trace.inputs["dst"],
                from_address=trace.from_address,
                token_address=trace.to_address,
            )
        else:
            return cls(
                transaction_hash=trace.transaction_hash,
                trace_address=trace.trace_address,
                amount=trace.inputs["amount"],
                to_address=trace.inputs["recipient"],
                from_address=trace.inputs.get("sender", trace.from_address),
                token_address=trace.to_address,
            )


#  -------- Liquidations ------------------------------------------------------------------------------


class LiquidationType(Enum):
    compound_v2_ceth_liquidation = "compound_v2_ceth_liquidation"
    compound_v2_ctoken_liquidation = "compound_v2_ctoken_liquidation"  # TODO: add logic to handle ctoken liquidations


class LiquidationStatus(Enum):
    seized = "seized"  # succesfully completed
    check = "check"  # just a liquidation check. i.e searcher only checks if opportunity is still available and reverts accordingly
    out_of_gas = "out_of_gas"  # tx ran out of gas


class LiquidationCollateralSource(Enum):
    aave_flashloan = "aave_flashloan"
    dydx_flashloan = "dydx_flashloan"
    uniswap_flashloan = "uniswap_flashloan"
    searcher_eoa = "searcher_eoa"  # searchers own funds
    searcher_contract = "searcher_contract"
    other = "other"


class Liquidation(CamelModel):
    tx_hash: str
    borrower: str  # account that got liquidated
    collateral_provided: str  # collateral provided by searcher, 'ether' or token contract address
    collateral_provided_amount: int  # amount of collateral provided
    asset_seized: str  # asset that was given to searcher at a discount upon liquidation
    asset_seized_amount: int  # amount of asset that was given to searcher upon liquidation
    profit_in_eth: int  # profit estimated by strategy inspector
    tokenflow_estimate_in_eth: int  # profit estimated by tokenflow
    tokenflow_diff: int  # diff between tokenflow and strategy inspector
    status: LiquidationStatus
    type: LiquidationType
    collateral_source: LiquidationCollateralSource


#  -------- Config ------------------------------------------------------------------------------


class ClassifierSpec(BaseModel):
    abi_name: str
    protocol: Optional[Protocol] = None
    valid_contract_addresses: Optional[List[str]] = None
    classifications: Dict[str, Classification] = {}
