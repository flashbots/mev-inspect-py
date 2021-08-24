# from enum import Enum
from .utils import CamelModel


class Tokenflow(CamelModel):
    tx_hash: str
    dollar_inflow: int
    dollar_outflow: int
    ether_inflow: int
    ether_outflow: int


class TokenflowSpecifc(CamelModel):
    tx_hash: str
    token_address: str
    token_inflow: int
    token_outflow: int
