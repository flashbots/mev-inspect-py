from sqlalchemy import ARRAY, Column, Integer, Numeric, String

from .base import Base


class TransferModel(Base):
    __tablename__ = "transfers"

    block_number = Column(Numeric, nullable=False)
    transaction_hash = Column(String, primary_key=True)
    trace_address = Column(ARRAY(Integer), nullable=False)
    protocol = Column(String, nullable=True)
    from_address = Column(String, nullable=False)
    to_address = Column(String, nullable=False)
    token_address = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    error = Column(String, nullable=True)
