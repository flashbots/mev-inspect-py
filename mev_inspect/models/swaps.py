from sqlalchemy import Column, Numeric, String, ARRAY, Integer

from .base import Base


class SwapModel(Base):
    __tablename__ = "swaps"

    abi_name = Column(String, nullable=False)
    transaction_hash = Column(String, primary_key=True)
    block_number = Column(Numeric, nullable=False)
    trace_address = Column(ARRAY(Integer), nullable=False)
    protocol = Column(String, nullable=True)
    pool_address = Column(String, nullable=False)
    from_address = Column(String, nullable=False)
    to_address = Column(String, nullable=False)
    token_in_address = Column(String, nullable=False)
    token_in_amount = Column(Numeric, nullable=False)
    token_out_address = Column(String, nullable=False)
    token_out_amount = Column(Numeric, nullable=False)
    error = Column(String, nullable=True)
