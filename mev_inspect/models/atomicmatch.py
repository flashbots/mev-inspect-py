from sqlalchemy import Column, Numeric, String, Integer, ARRAY

from .base import Base


class AtomicMatchModel(Base):
    __tablename__ = "atomic_match"

    block_number = Column(Numeric, nullable=False)
    transaction_hash = Column(String, primary_key=True)
    protocol = Column(String, nullable=True)
    from_address = Column(String, nullable=False)
    to_address = Column(String, nullable=False)
    token_address = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    metadata = Column(ARRAY(String), nullable=False)
    error = Column(String, nullable=True)
