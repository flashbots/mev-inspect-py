from mev_inspect.schemas.classified_traces import (
    DecodedCallTrace,
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    AtomicMatchClassifier,
)

OPENSEA_ATOMIC_MATCH_ABI_NAME='atomicMatch_'

OPENSEA_SPEC = [
    ClassifierSpec(
        abi_name="atomicMatch_",
        protocol=Protocol.opensea,
        valid_contract_addresses=["0x7be8076f4ea4a4ad08075c2508e481d6c946d12b"],
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

UNISWAP_CLASSIFIER_SPECS = [
    *UNISWAP_V3_CONTRACT_SPECS,
    *UNISWAPPY_V2_CONTRACT_SPECS,
    *UNISWAP_V3_GENERAL_SPECS,
    UNISWAPPY_V2_PAIR_SPEC,
]
