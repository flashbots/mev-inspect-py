from enum import Enum
from hexbytes._utils import hexstr_to_bytes


class RPCType(Enum):
    parity = 0
    geth = 1


def hex_to_int(value: str) -> int:
    return int.from_bytes(hexstr_to_bytes(value), byteorder="big")
