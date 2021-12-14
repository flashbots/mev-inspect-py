from enum import Enum
from typing import List, Optional, Union

import eth_utils.abi
from pydantic import BaseModel
from typing_extensions import Literal
from web3 import Web3


class ABIDescriptionType(str, Enum):
    function = "function"
    constructor = "constructor"
    fallback = "fallback"
    event = "event"
    receive = "receive"


NON_FUNCTION_DESCRIPTION_TYPES = Union[
    Literal[ABIDescriptionType.constructor],
    Literal[ABIDescriptionType.fallback],
    Literal[ABIDescriptionType.event],
    Literal[ABIDescriptionType.receive],
]


class ABIDescriptionInput(BaseModel):
    name: str
    type: str
    components: Optional[List["ABIDescriptionInput"]]


ABIDescriptionInput.update_forward_refs()


class ABIGenericDescription(BaseModel):
    type: NON_FUNCTION_DESCRIPTION_TYPES


class ABIFunctionDescription(BaseModel):
    type: Literal[ABIDescriptionType.function]
    name: str
    inputs: List[ABIDescriptionInput]

    def get_selector(self) -> str:
        signature = self.get_signature()
        return Web3.sha3(text=signature)[0:4].hex()

    def get_signature(self) -> str:
        joined_input_types = ",".join(
            input.type
            if input.type != "tuple"
            else eth_utils.abi.collapse_if_tuple(input.dict())
            for input in self.inputs
        )
        return f"{self.name}({joined_input_types})"


ABIDescription = Union[ABIFunctionDescription, ABIGenericDescription]
ABI = List[ABIDescription]
