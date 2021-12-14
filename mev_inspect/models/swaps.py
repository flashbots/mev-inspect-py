from sqlalchemy import ARRAY, Column, Integer, Numeric, String

from .base import Base


class SwapModel(Base):
    __tablename__ = "swaps"

    abi_name = Column(String, nullable=False)
    transaction_hash = Column(String, primary_key=True)
    transaction_position = Column(Numeric, nullable=True)
    block_number = Column(Numeric, nullable=False)
    trace_address = Column(ARRAY(Integer), nullable=False)
    protocol = Column(String, nullable=True)
    contract_address = Column(String, nullable=False)
    from_address = Column(String, nullable=False)
    to_address = Column(String, nullable=False)
    token_in_address = Column(String, nullable=False)
    token_in_amount = Column(Numeric, nullable=False)
    token_out_address = Column(String, nullable=False)
    token_out_amount = Column(Numeric, nullable=False)
    error = Column(String, nullable=True)
