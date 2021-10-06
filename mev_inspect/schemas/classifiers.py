from typing import Callable, Dict, List, Optional, Union
from typing_extensions import Literal

from pydantic import BaseModel

from .classified_traces import Classification, DecodedCallTrace, Protocol
from .transfers import Transfer


class TransferClassifier(BaseModel):
    classification: Literal[Classification.transfer] = Classification.transfer
    get_transfer: Callable[[DecodedCallTrace], Transfer]


class SwapClassifier(BaseModel):
    classification: Literal[Classification.swap] = Classification.swap


class LiquidationClassifier(BaseModel):
    classification: Literal[Classification.liquidate] = Classification.liquidate


Classifier = Union[TransferClassifier, SwapClassifier, LiquidationClassifier]


class ClassifierSpec(BaseModel):
    abi_name: str
    protocol: Optional[Protocol] = None
    valid_contract_addresses: Optional[List[str]] = None
    classifiers: Dict[str, Classifier] = {}
