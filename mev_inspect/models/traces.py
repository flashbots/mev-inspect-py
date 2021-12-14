from sqlalchemy import ARRAY, JSON, Column, Integer, Numeric, String

from .base import Base


class ClassifiedTraceModel(Base):
    __tablename__ = "classified_traces"

    transaction_hash = Column(String, primary_key=True)
    transaction_position = Column(Numeric, nullable=True)
    block_number = Column(Numeric, nullable=False)
    classification = Column(String, nullable=False)
    trace_type = Column(String, nullable=False)
    trace_address = Column(ARRAY(Integer), nullable=False)
    protocol = Column(String, nullable=True)
    abi_name = Column(String, nullable=True)
    function_name = Column(String, nullable=True)
    function_signature = Column(String, nullable=True)
    inputs = Column(JSON, nullable=True)
    from_address = Column(String, nullable=True)
    to_address = Column(String, nullable=True)
    gas = Column(Numeric, nullable=True)
    value = Column(Numeric, nullable=True)
    gas_used = Column(Numeric, nullable=True)
    error = Column(String, nullable=True)
