from sqlalchemy import Column, Numeric, String

from .base import Base


class SwapModel(Base):
    __tablename__ = "swaps"

    block_number = Column(Numeric, nullable=False)
    transaction_hash = Column(String, primary_key=True)
    transaction_index = Column(Numeric, nullable=False)
    miner_address = Column(String, nullable=False)
    coinbase_transfer = Column(Numeric, nullable=False)
    base_fee_per_gas = Column(Numeric, nullable=False)
    gas_price = Column(Numeric, nullable=False)
    gas_price_with_coinbase_transfer = Column(Numeric, nullable=False)
    gas_used = Column(Numeric, nullable=False)
