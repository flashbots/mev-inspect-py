from typing import Dict, Optional

import eth_utils.abi
from eth_abi import decode_abi
from eth_abi.exceptions import InsufficientDataBytes, NonEmptyPaddingBytes
from hexbytes._utils import hexstr_to_bytes

from mev_inspect.schemas.abi import ABI, ABIFunctionDescription
from mev_inspect.schemas.call_data import CallData

# 0x + 8 characters
SELECTOR_LENGTH = 10


class ABIDecoder:
    def __init__(self, abi: ABI):
        self._functions_by_selector: Dict[str, ABIFunctionDescription] = {
            description.get_selector(): description
            for description in abi
            if isinstance(description, ABIFunctionDescription)
        }

    def decode(self, data: str) -> Optional[CallData]:
        selector, params = data[:SELECTOR_LENGTH], data[SELECTOR_LENGTH:]

        func = self._functions_by_selector.get(selector)

        if func is None:
            return None

        names = [input.name for input in func.inputs]
        types = [
            input.type
            if input.type != "tuple"
            else eth_utils.abi.collapse_if_tuple(input.dict())
            for input in func.inputs
        ]

        try:
            decoded = decode_abi(types, hexstr_to_bytes(params))
        except (InsufficientDataBytes, NonEmptyPaddingBytes, OverflowError):
            return None

        return CallData(
            function_name=func.name,
            function_signature=func.get_signature(),
            inputs={name: value for name, value in zip(names, decoded)},
        )
