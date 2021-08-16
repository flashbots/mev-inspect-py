from typing import Dict, Optional

from hexbytes import HexBytes
from eth_abi import decode_abi
from eth_abi.exceptions import InsufficientDataBytes, NonEmptyPaddingBytes

from mev_inspect.schemas.abi import ABI, ABIFunctionDescription
from mev_inspect.schemas.call_data import CallData


class ABIDecoder:
    def __init__(self, abi: ABI):
        self._functions_by_selector: Dict[str, ABIFunctionDescription] = {
            description.get_selector(): description
            for description in abi
            if isinstance(description, ABIFunctionDescription)
        }

    def decode(self, data: str) -> Optional[CallData]:
        hex_data = HexBytes(data)
        selector, params = hex_data[:4], hex_data[4:]

        func = self._functions_by_selector.get(selector)

        if func is None:
            return None

        names = [input.name for input in func.inputs]
        types = [input.type for input in func.inputs]

        try:
            decoded = decode_abi(types, params)
        except (InsufficientDataBytes, NonEmptyPaddingBytes):
            return None

        return CallData(
            function_name=func.name,
            function_signature=func.get_signature(),
            inputs={name: value for name, value in zip(names, decoded)},
        )
