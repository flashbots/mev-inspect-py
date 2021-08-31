from sqlalchemy import Column, Numeric, String

from .base import Base


class MinerPaymentModel(Base):
    __tablename__ = "miner_payments"

    block_number = Column(Numeric, nullable=False)
    transaction_hash = Column(String, primary_key=True)
    transaction_index = Column(Numeric, nullable=False)
    miner_address = Column(String, nullable=False)
    coinbase_transfer = Column(Numeric, nullable=False)
    base_fee_per_gas = Column(Numeric, nullable=False)
    gas_price = Column(Numeric, nullable=False)
    gas_price_with_coinbase_transfer = Column(Numeric, nullable=False)
    gas_used = Column(Numeric, nullable=False)
    transaction_from_address = Column(String, nullable=True)
    transaction_to_address = Column(String, nullable=True)
