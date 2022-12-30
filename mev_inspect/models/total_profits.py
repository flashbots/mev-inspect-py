from sqlalchemy import Column, Integer, Numeric, String

from .base import Base


class TotalProfitsModel(Base):
    __tablename__ = "total_profit_by_block"

    id = Column("id", Integer, nullable=False, autoincrement=True, primary_key=True)
    block_number = Column("block_number", Numeric, nullable=False)
    transaction_hash = Column("transaction_hash", String(66), nullable=False)
    token_debt = Column("token_debt", String(66), nullable=True)
    amount_debt = Column("amount_debt", Numeric, nullable=False)
    token_received = Column("token_received", String(66), nullable=False)
    amount_received = Column("amount_received", Numeric, nullable=False)
