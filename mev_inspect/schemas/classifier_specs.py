from typing import Callable, Dict, List, Optional

from pydantic import BaseModel

from .classified_traces import Classification, DecodedCallTrace, Protocol
from .transfers import ERC20Transfer


TransferClassifier = Callable[[DecodedCallTrace], Optional[ERC20Transfer]]


class ClassifierSpec(BaseModel):
    abi_name: str
    protocol: Optional[Protocol] = None
    valid_contract_addresses: Optional[List[str]] = None
    classifications: Dict[str, Classification] = {}
    transfer_classifiers: Dict[str, TransferClassifier] = {}
