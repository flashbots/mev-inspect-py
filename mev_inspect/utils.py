from hexbytes._utils import hexstr_to_bytes


def hex_to_int(value: str) -> int:
    return int.from_bytes(hexstr_to_bytes(value), byteorder="big")
