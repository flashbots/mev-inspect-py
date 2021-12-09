from typing import Dict, Optional, Tuple, Type

from mev_inspect.schemas.traces import DecodedCallTrace, Protocol
from mev_inspect.schemas.classifiers import ClassifierSpec, Classifier

from .aave import AAVE_CLASSIFIER_SPECS
from .curve import CURVE_CLASSIFIER_SPECS
from .erc20 import ERC20_CLASSIFIER_SPECS
from .uniswap import UNISWAP_CLASSIFIER_SPECS
from .weth import WETH_CLASSIFIER_SPECS, WETH_ADDRESS
from .zero_ex import ZEROX_CLASSIFIER_SPECS
from .balancer import BALANCER_CLASSIFIER_SPECS
from .compound import COMPOUND_CLASSIFIER_SPECS
from .cryptopunks import CRYPTOPUNKS_CLASSIFIER_SPECS
from .bancor import BANCOR_CLASSIFIER_SPECS

ALL_CLASSIFIER_SPECS = (
    ERC20_CLASSIFIER_SPECS
    + WETH_CLASSIFIER_SPECS
    + CURVE_CLASSIFIER_SPECS
    + UNISWAP_CLASSIFIER_SPECS
    + AAVE_CLASSIFIER_SPECS
    + ZEROX_CLASSIFIER_SPECS
    + BALANCER_CLASSIFIER_SPECS
    + COMPOUND_CLASSIFIER_SPECS
    + CRYPTOPUNKS_CLASSIFIER_SPECS
    + BANCOR_CLASSIFIER_SPECS
)

_SPECS_BY_ABI_NAME_AND_PROTOCOL: Dict[
    Tuple[str, Optional[Protocol]], ClassifierSpec
] = {(spec.abi_name, spec.protocol): spec for spec in ALL_CLASSIFIER_SPECS}


def get_classifier(
    trace: DecodedCallTrace,
) -> Optional[Type[Classifier]]:
    abi_name_and_protocol = (trace.abi_name, trace.protocol)
    spec = _SPECS_BY_ABI_NAME_AND_PROTOCOL.get(abi_name_and_protocol)

    if spec is not None:
        return spec.classifiers.get(trace.function_signature)

    return None
