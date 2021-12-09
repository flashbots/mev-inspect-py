from sqlalchemy import Column, Numeric, String, ARRAY, Integer

from .base import Base


class PunkSnipeModel(Base):
    __tablename__ = "punk_snipes"

    block_number = Column(Numeric, nullable=False)
    transaction_hash = Column(String, primary_key=True)
    trace_address = Column(ARRAY(Integer), primary_key=True)
    from_address = Column(String, nullable=False)
    punk_index = Column(Integer, nullable=False)
    min_acceptance_price = Column(Numeric, nullable=False)
    acceptance_price = Column(Numeric, nullable=False)
