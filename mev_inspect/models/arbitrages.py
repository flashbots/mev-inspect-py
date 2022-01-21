from sqlalchemy import ARRAY, Column, Numeric, String

from .base import Base


class ArbitrageModel(Base):
    __tablename__ = "arbitrages"

    id = Column(String, primary_key=True)
    block_number = Column(Numeric, nullable=False)
    transaction_hash = Column(String, nullable=False)
    account_address = Column(String, nullable=False)
    profit_token_address = Column(String, nullable=False)
    start_amount = Column(Numeric, nullable=False)
    end_amount = Column(Numeric, nullable=False)
    profit_amount = Column(Numeric, nullable=False)
    error = Column(String, nullable=True)
    protocols = Column(ARRAY(String))
