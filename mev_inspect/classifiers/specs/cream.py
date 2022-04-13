from typing import List, Optional

from mev_inspect.classifiers.helpers import get_debt_transfer, get_received_transfer
from mev_inspect.schemas.classifiers import (
    Classification,
    ClassifiedTrace,
    ClassifierSpec,
    DecodedCallTrace,
    LiquidationClassifier,
    SeizeClassifier,
)
from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.prices import ETH_TOKEN_ADDRESS
from mev_inspect.schemas.traces import Protocol
from mev_inspect.schemas.transfers import Transfer

CRETH_TOKEN_ADDRESS = "0xd06527d5e56a3495252a528c4987003b712860ee"


class CreamLiquidationClassifier(LiquidationClassifier):
    @staticmethod
    def parse_liquidation(
        liquidation_trace: DecodedCallTrace,
        child_transfers: List[Transfer],
        child_traces: List[ClassifiedTrace],
    ) -> Optional[Liquidation]:

        liquidator = liquidation_trace.from_address
        liquidated = liquidation_trace.inputs["borrower"]

        debt_token_address = liquidation_trace.to_address
        received_token_address = liquidation_trace.inputs["cTokenCollateral"]

        debt_purchase_amount = None
        received_amount = None

        debt_purchase_amount, debt_token_address = (
            (liquidation_trace.value, ETH_TOKEN_ADDRESS)
            if debt_token_address == CRETH_TOKEN_ADDRESS
            and liquidation_trace.value != 0
            else (liquidation_trace.inputs["repayAmount"], CRETH_TOKEN_ADDRESS)
        )

        debt_transfer = get_debt_transfer(liquidator, child_transfers)

        received_transfer = get_received_transfer(liquidator, child_transfers)

        seize_trace = _get_seize_call(child_traces)

        if debt_transfer is not None:
            debt_token_address = debt_transfer.token_address
            debt_purchase_amount = debt_transfer.amount

        if received_transfer is not None:
            received_token_address = received_transfer.token_address
            received_amount = received_transfer.amount

        elif seize_trace is not None and seize_trace.inputs is not None:
            received_amount = seize_trace.inputs["seizeTokens"]

        if received_amount is None:
            return None

        return Liquidation(
            liquidated_user=liquidated,
            debt_token_address=debt_token_address,
            liquidator_user=liquidator,
            debt_purchase_amount=debt_purchase_amount,
            protocol=liquidation_trace.protocol,
            received_amount=received_amount,
            received_token_address=received_token_address,
            transaction_hash=liquidation_trace.transaction_hash,
            trace_address=liquidation_trace.trace_address,
            block_number=liquidation_trace.block_number,
            error=liquidation_trace.error,
        )

        return None


CREAM_CRETH_SPEC = ClassifierSpec(
    abi_name="CEther",
    protocol=Protocol.cream,
    valid_contract_addresses=["0xD06527D5e56A3495252A528C4987003b712860eE"],
    classifiers={
        "liquidateBorrow(address,address)": CreamLiquidationClassifier,
        "seize(address,address,uint256)": SeizeClassifier,
    },
)

CREAM_CTOKEN_SPEC = ClassifierSpec(
    abi_name="CToken",
    protocol=Protocol.cream,
    valid_contract_addresses=[
        "0xd06527d5e56a3495252a528c4987003b712860ee",
        "0x51f48b638f82e8765f7a26373a2cb4ccb10c07af",
        "0x44fbebd2f576670a6c33f6fc0b00aa8c5753b322",
        "0xcbae0a83f4f9926997c8339545fb8ee32edc6b76",
        "0xce4fe9b4b8ff61949dcfeb7e03bc9faca59d2eb3",
        "0x19d1666f543d42ef17f66e376944a22aea1a8e46",
        "0x9baf8a5236d44ac410c0186fe39178d5aad0bb87",
        "0x797aab1ce7c01eb727ab980762ba88e7133d2157",
        "0x892b14321a4fcba80669ae30bd0cd99a7ecf6ac0",
        "0x697256caa3ccafd62bb6d3aa1c7c5671786a5fd9",
        "0x8b86e0598616a8d4f1fdae8b59e55fb5bc33d0d6",
        "0xc7fd8dcee4697ceef5a2fd4608a7bd6a94c77480",
        "0x17107f40d70f4470d20cb3f138a052cae8ebd4be",
        "0x1ff8cdb51219a8838b52e9cac09b71e591bc998e",
        "0x3623387773010d9214b10c551d6e7fc375d31f58",
        "0x4ee15f44c6f0d8d1136c83efd2e8e4ac768954c6",
        "0x338286c0bc081891a4bda39c7667ae150bf5d206",
        "0x10fdbd1e48ee2fd9336a482d746138ae19e649db",
        "0x01da76dea59703578040012357b81ffe62015c2d",
        "0xef58b2d5a1b8d3cde67b8ab054dc5c831e9bc025",
        "0xe89a6d0509faf730bd707bf868d9a2a744a363c7",
        "0xeff039c3c1d668f408d09dd7b63008622a77532c",
        "0x22b243b96495c547598d9042b6f94b01c22b2e9e",
        "0x8b3ff1ed4f36c2c2be675afb13cc3aa5d73685a5",
        "0x2a537fa9ffaea8c1a41d3c2b68a9cb791529366d",
        "0x7ea9c63e216d5565c3940a2b3d150e59c2907db3",
        "0x3225e3c669b39c7c8b3e204a8614bb218c5e31bc",
        "0xf55bbe0255f7f4e70f63837ff72a577fbddbe924",
        "0x903560b1cce601794c584f58898da8a8b789fc5d",
        "0x054b7ed3f45714d3091e82aad64a1588dc4096ed",
        "0xd5103afcd0b3fa865997ef2984c66742c51b2a8b",
        "0xfd609a03b393f1a1cfcacedabf068cad09a924e2",
        "0xd692ac3245bb82319a31068d6b8412796ee85d2c",
        "0x92b767185fb3b04f881e3ac8e5b0662a027a1d9f",
        "0x10a3da2bb0fae4d591476fd97d6636fd172923a8",
        "0x3c6c553a95910f9fc81c98784736bd628636d296",
        "0x21011bc93d9e515b9511a817a1ed1d6d468f49fc",
        "0x85759961b116f1d36fd697855c57a6ae40793d9b",
        "0x7c3297cfb4c4bbd5f44b450c0872e0ada5203112",
        "0x7aaa323d7e398be4128c7042d197a2545f0f1fea",
        "0x011a014d5e8eb4771e575bb1000318d509230afa",
        "0xe6c3120f38f56deb38b69b65cc7dcaf916373963",
        "0x4fe11bc316b6d7a345493127fbe298b95adaad85",
        "0xcd22c4110c12ac41acefa0091c432ef44efaafa0",
        "0x228619cca194fbe3ebeb2f835ec1ea5080dafbb2",
        "0x73f6cba38922960b7092175c0add22ab8d0e81fc",
        "0x38f27c03d6609a86ff7716ad03038881320be4ad",
        "0x5ecad8a75216cea7dff978525b2d523a251eea92",
        "0x5c291bc83d15f71fb37805878161718ea4b6aee9",
        "0x6ba0c66c48641e220cf78177c144323b3838d375",
        "0xd532944df6dfd5dd629e8772f03d4fc861873abf",
        "0x197070723ce0d3810a0e47f06e935c30a480d4fc",
        "0xc25eae724f189ba9030b2556a1533e7c8a732e14",
        "0x25555933a8246ab67cbf907ce3d1949884e82b55",
        "0xc68251421edda00a10815e273fa4b1191fac651b",
        "0x65883978ada0e707c3b2be2a6825b1c4bdf76a90",
        "0x8b950f43fcac4931d408f1fcda55c6cb6cbf3096",
        "0x59089279987dd76fc65bf94cb40e186b96e03cb3",
        "0x2db6c82ce72c8d7d770ba1b5f5ed0b6e075066d6",
        "0xb092b4601850e23903a42eacbc9d8a0eec26a4d5",
        "0x081fe64df6dc6fc70043aedf3713a3ce6f190a21",
        "0x1d0986fb43985c88ffa9ad959cc24e6a087c7e35",
        "0xc36080892c64821fa8e396bc1bd8678fa3b82b17",
        "0x8379baa817c5c5ab929b03ee8e3c48e45018ae41",
        "0x299e254a8a165bbeb76d9d69305013329eea3a3b",
        "0xf8445c529d363ce114148662387eba5e62016e20",
        "0x28526bb33d7230e65e735db64296413731c5402e",
        "0x45406ba53bb84cd32a58e7098a2d4d1b11b107f6",
        "0x6d1b9e01af17dd08d6dec08e210dfd5984ff1c20",
        "0x1f9b4756b008106c806c7e64322d7ed3b72cb284",
        "0xab10586c918612ba440482db77549d26b7abf8f7",
        "0xdfff11dfe6436e42a17b86e7f419ac8292990393",
        "0xdbb5e3081def4b6cdd8864ac2aeda4cbf778fecf",
        "0x71cefcd324b732d4e058afacba040d908c441847",
        "0x1a122348b73b58ea39f822a89e6ec67950c2bbd0",
        "0x523effc8bfefc2948211a05a905f761cba5e8e9e",
        "0x4202d97e00b9189936edf37f8d01cff88bdd81d4",
        "0x4baa77013ccd6705ab0522853cb0e9d453579dd4",
        "0x98e329eb5aae2125af273102f3440de19094b77c",
        "0x8c3b7a4320ba70f8239f83770c4015b5bc4e6f91",
        "0xe585c76573d7593abf21537b607091f76c996e73",
        "0x81e346729723c4d15d0fb1c5679b9f2926ff13c6",
        "0x766175eac1a99c969ddd1ebdbe7e270d508d8fff",
        "0xd7394428536f63d5659cc869ef69d10f9e66314b",
        "0x1241b10e7ea55b22f5b2d007e8fecdf73dcff999",
        "0x2a867fd776b83e1bd4e13c6611afd2f6af07ea6d",
        "0x250fb308199fe8c5220509c1bf83d21d60b7f74a",
        "0x4112a717edd051f77d834a6703a1ef5e3d73387f",
        "0xf04ce2e71d32d789a259428ddcd02d3c9f97fb4e",
        "0x89e42987c39f72e2ead95a8a5bc92114323d5828",
        "0x58da9c9fc3eb30abbcbbab5ddabb1e6e2ef3d2ef",
    ],
    classifiers={
        "liquidateBorrow(address,uint256,address)": CreamLiquidationClassifier,
        "seize(address,address,uint256)": SeizeClassifier,
    },
)

CREAM_CLASSIFIER_SPECS: List[ClassifierSpec] = [
    CREAM_CRETH_SPEC,
    CREAM_CTOKEN_SPEC,
]


def _get_seize_call(traces: List[ClassifiedTrace]) -> Optional[ClassifiedTrace]:
    """Find the call to `seize` in the child traces (successful liquidation)"""
    for trace in traces:
        if trace.classification == Classification.seize:
            return trace
    return None
