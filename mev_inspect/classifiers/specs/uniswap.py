from typing import Optional, List
from mev_inspect.schemas.transfers import Transfer
from mev_inspect.schemas.swaps import Swap
from mev_inspect.schemas.traces import (
    DecodedCallTrace,
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    SwapClassifier,
)
from mev_inspect.classifiers.helpers import create_swap_from_pool_transfers


UNISWAP_V2_PAIR_ABI_NAME = "UniswapV2Pair"
UNISWAP_V3_POOL_ABI_NAME = "UniswapV3Pool"


class UniswapV3SwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        trace: DecodedCallTrace,
        prior_transfers: List[Transfer],
        child_transfers: List[Transfer],
    ) -> Optional[Swap]:

        recipient_address = trace.inputs.get("recipient", trace.from_address)

        swap = create_swap_from_pool_transfers(
            trace, recipient_address, prior_transfers, child_transfers
        )
        return swap


class UniswapV2SwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        trace: DecodedCallTrace,
        prior_transfers: List[Transfer],
        child_transfers: List[Transfer],
    ) -> Optional[Swap]:

        recipient_address = trace.inputs.get("to", trace.from_address)

        swap = create_swap_from_pool_transfers(
            trace, recipient_address, prior_transfers, child_transfers
        )
        return swap


UNISWAP_V3_CONTRACT_SPECS = [
    ClassifierSpec(
        abi_name="UniswapV3Factory",
        protocol=Protocol.uniswap_v3,
        valid_contract_addresses=["0x1F98431c8aD98523631AE4a59f267346ea31F984"],
    ),
    ClassifierSpec(
        abi_name="Multicall2",
        protocol=Protocol.uniswap_v3,
        valid_contract_addresses=["0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696"],
    ),
    ClassifierSpec(
        abi_name="ProxyAdmin",
        protocol=Protocol.uniswap_v3,
        valid_contract_addresses=["0xB753548F6E010e7e680BA186F9Ca1BdAB2E90cf2"],
    ),
    ClassifierSpec(
        abi_name="TickLens",
        protocol=Protocol.uniswap_v3,
        valid_contract_addresses=["0xbfd8137f7d1516D3ea5cA83523914859ec47F573"],
    ),
    ClassifierSpec(
        abi_name="Quoter",
        protocol=Protocol.uniswap_v3,
        valid_contract_addresses=["0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6"],
    ),
    ClassifierSpec(
        abi_name="SwapRouter",
        protocol=Protocol.uniswap_v3,
        valid_contract_addresses=["0xE592427A0AEce92De3Edee1F18E0157C05861564"],
    ),
    ClassifierSpec(
        abi_name="NFTDescriptor",
        protocol=Protocol.uniswap_v3,
        valid_contract_addresses=["0x42B24A95702b9986e82d421cC3568932790A48Ec"],
    ),
    ClassifierSpec(
        abi_name="NonfungibleTokenPositionDescriptor",
        protocol=Protocol.uniswap_v3,
        valid_contract_addresses=["0x91ae842A5Ffd8d12023116943e72A606179294f3"],
    ),
    ClassifierSpec(
        abi_name="TransparentUpgradeableProxy",
        protocol=Protocol.uniswap_v3,
        valid_contract_addresses=["0xEe6A57eC80ea46401049E92587E52f5Ec1c24785"],
    ),
    ClassifierSpec(
        abi_name="NonfungiblePositionManager",
        protocol=Protocol.uniswap_v3,
        valid_contract_addresses=["0xC36442b4a4522E871399CD717aBDD847Ab11FE88"],
    ),
    ClassifierSpec(
        abi_name="V3Migrator",
        protocol=Protocol.uniswap_v3,
        valid_contract_addresses=["0xA5644E29708357803b5A882D272c41cC0dF92B34"],
    ),
]

UNISWAP_V3_GENERAL_SPECS = [
    ClassifierSpec(
        abi_name=UNISWAP_V3_POOL_ABI_NAME,
        classifiers={
            "swap(address,bool,int256,uint160,bytes)": UniswapV3SwapClassifier,
        },
    ),
    ClassifierSpec(
        abi_name="IUniswapV3SwapCallback",
    ),
    ClassifierSpec(
        abi_name="IUniswapV3MintCallback",
    ),
    ClassifierSpec(
        abi_name="IUniswapV3FlashCallback",
    ),
]


UNISWAPPY_V2_CONTRACT_SPECS = [
    ClassifierSpec(
        abi_name="UniswapV2Router",
        protocol=Protocol.uniswap_v2,
        valid_contract_addresses=["0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"],
    ),
    ClassifierSpec(
        abi_name="UniswapV2Router",
        protocol=Protocol.sushiswap,
        valid_contract_addresses=["0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"],
    ),
]

UNISWAPPY_V2_PAIR_SPEC = ClassifierSpec(
    abi_name=UNISWAP_V2_PAIR_ABI_NAME,
    classifiers={
        "swap(uint256,uint256,address,bytes)": UniswapV2SwapClassifier,
    },
)

UNISWAP_CLASSIFIER_SPECS: List = [
    *UNISWAP_V3_CONTRACT_SPECS,
    *UNISWAPPY_V2_CONTRACT_SPECS,
    *UNISWAP_V3_GENERAL_SPECS,
    UNISWAPPY_V2_PAIR_SPEC,
]
