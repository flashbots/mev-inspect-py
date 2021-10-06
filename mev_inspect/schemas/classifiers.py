from typing import Dict, List, Optional
from typing_extensions import Literal

from pydantic import BaseModel

from .classified_traces import Classification, Protocol


class Classifier(BaseModel):
    classification: Classification


class TransferClassifier(Classifier):
    classification: Literal[Classification.transfer] = Classification.transfer


class SwapClassifier(Classifier):
    classification: Literal[Classification.swap] = Classification.swap


class LiquidationClassifier(Classifier):
    classification: Literal[Classification.liquidate] = Classification.liquidate


class ClassifierSpec(BaseModel):
    abi_name: str
    protocol: Optional[Protocol] = None
    valid_contract_addresses: Optional[List[str]] = None
    classifiers: Dict[str, Classifier] = {}
