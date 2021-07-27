from hexbytes.main import HexBytes


def hex_to_int(value: str) -> int:
    return int.from_bytes(HexBytes(value), byteorder="big")
