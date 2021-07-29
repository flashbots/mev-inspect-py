from mev_inspect.schemas.classified_traces import (
    Classification,
    ClassifierSpec,
    Protocol,
)


SUSHISWAP_ROUTER_ADDRESS = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
UNISWAP_V2_ROUTER_ADDRESS = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"


CLASSIFIER_SPECS = [
    ClassifierSpec(
        abi_name="UniswapV2Router",
        protocol=Protocol.uniswap_v2,
        valid_contract_addresses=[UNISWAP_V2_ROUTER_ADDRESS],
    ),
    ClassifierSpec(
        abi_name="UniswapV2Router",
        protocol=Protocol.sushiswap,
        valid_contract_addresses=[SUSHISWAP_ROUTER_ADDRESS],
    ),
    ClassifierSpec(
        abi_name="ERC20",
        classifications={
            "transferFrom(address,address,uint256)": Classification.transfer,
            "transfer(address,uint256)": Classification.transfer,
            "burn(address)": Classification.burn,
        },
    ),
    ClassifierSpec(
        abi_name="UniswapV2Pair",
        classifications={
            "swap(uint256,uint256,address,bytes)": Classification.swap,
        },
    ),
]
