from sqlalchemy import Column, Numeric, String, func, TIMESTAMP, ARRAY, Integer

from .base import Base


class SandwichModel(Base):
    __tablename__ = "sandwiches"

    id = Column(String, primary_key=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    block_number = Column(Numeric, nullable=False)
    sandwicher_address = Column(String(256), nullable=False)
    frontrun_swap_transaction_hash = Column(String(256), nullable=False)
    frontrun_swap_trace_address = Column(ARRAY(Integer), nullable=False)
    backrun_swap_transaction_hash = Column(String(256), nullable=False)
    backrun_swap_trace_address = Column(ARRAY(Integer), nullable=False)
