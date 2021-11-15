from typing import Optional, List, Sequence

from mev_inspect.schemas.traces import (
    ClassifiedTrace,
    DecodedCallTrace,
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    SwapClassifier,
)

from mev_inspect.schemas.swaps import Swap
from mev_inspect.schemas.transfers import Transfer, ETH_TOKEN_ADDRESS

UNISWAP_V2_PAIR_ABI_NAME = "UniswapV2Pair"
UNISWAP_V3_POOL_ABI_NAME = "UniswapV3Pool"


class UniswapV3SwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        trace: DecodedCallTrace,
        prior_transfers: List[Transfer],
        child_transfers: List[Transfer],
    ) -> Optional[Swap]:
        pool_address = trace.to_address

        if trace.inputs is not None and "recipient" in trace.inputs:
            recipient_address = trace.inputs["recipient"]
        else:
            recipient_address = trace.from_address

        if recipient_address is None:
            return None

        transfers_to_pool = []

        if trace.value is not None and trace.value > 0:
            transfers_to_pool = [_build_eth_transfer(trace)]

        if len(transfers_to_pool) == 0:
            transfers_to_pool = _filter_transfers(
                prior_transfers, to_address=pool_address
            )

        if len(transfers_to_pool) == 0:
            transfers_to_pool = _filter_transfers(
                child_transfers, to_address=pool_address
            )

        if len(transfers_to_pool) == 0:
            return None

        transfers_from_pool_to_recipient = _filter_transfers(
            child_transfers, to_address=recipient_address, from_address=pool_address
        )

        if len(transfers_from_pool_to_recipient) != 1:
            return None

        transfer_in = transfers_to_pool[-1]
        transfer_out = transfers_from_pool_to_recipient[0]

        return Swap(
            abi_name=trace.abi_name,
            transaction_hash=trace.transaction_hash,
            block_number=trace.block_number,
            trace_address=trace.trace_address,
            pool_address=pool_address,
            protocol=trace.protocol,
            from_address=transfer_in.from_address,
            to_address=transfer_out.to_address,
            token_in_address=transfer_in.token_address,
            token_in_amount=transfer_in.amount,
            token_out_address=transfer_out.token_address,
            token_out_amount=transfer_out.amount,
            error=trace.error,
        )


class UniswapV2SwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        trace: DecodedCallTrace,
        prior_transfers: List[Transfer],
        child_transfers: List[Transfer],
    ) -> Optional[Swap]:
        pool_address = trace.to_address

        if trace.inputs is not None and "to" in trace.inputs:
            recipient_address = trace.inputs["to"]
        else:
            recipient_address = trace.from_address

        if recipient_address is None:
            return None

        transfers_to_pool = []

        if trace.value is not None and trace.value > 0:
            transfers_to_pool = [_build_eth_transfer(trace)]

        if len(transfers_to_pool) == 0:
            transfers_to_pool = _filter_transfers(
                prior_transfers, to_address=pool_address
            )

        if len(transfers_to_pool) == 0:
            transfers_to_pool = _filter_transfers(
                child_transfers, to_address=pool_address
            )

        if len(transfers_to_pool) == 0:
            return None

        transfers_from_pool_to_recipient = _filter_transfers(
            child_transfers, to_address=recipient_address, from_address=pool_address
        )

        if len(transfers_from_pool_to_recipient) != 1:
            return None

        transfer_in = transfers_to_pool[-1]
        transfer_out = transfers_from_pool_to_recipient[0]

        return Swap(
            abi_name=trace.abi_name,
            transaction_hash=trace.transaction_hash,
            block_number=trace.block_number,
            trace_address=trace.trace_address,
            pool_address=pool_address,
            protocol=trace.protocol,
            from_address=transfer_in.from_address,
            to_address=transfer_out.to_address,
            token_in_address=transfer_in.token_address,
            token_in_amount=transfer_in.amount,
            token_out_address=transfer_out.token_address,
            token_out_amount=transfer_out.amount,
            error=trace.error,
        )


def _build_eth_transfer(trace: ClassifiedTrace) -> Transfer:
    return Transfer(
        block_number=trace.block_number,
        transaction_hash=trace.transaction_hash,
        trace_address=trace.trace_address,
        amount=trace.value,
        to_address=trace.to_address,
        from_address=trace.from_address,
        token_address=ETH_TOKEN_ADDRESS,
    )


def _filter_transfers(
    transfers: Sequence[Transfer],
    to_address: Optional[str] = None,
    from_address: Optional[str] = None,
) -> List[Transfer]:
    filtered_transfers = []

    for transfer in transfers:
        if to_address is not None and transfer.to_address != to_address:
            continue

        if from_address is not None and transfer.from_address != from_address:
            continue

        filtered_transfers.append(transfer)

    return filtered_transfers


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
