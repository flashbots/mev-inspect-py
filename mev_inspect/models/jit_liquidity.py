from sqlalchemy import ARRAY, Column, Integer, Numeric, String

from .base import Base


class JITLiquidityModel(Base):
    id = Column(String, primary_key=True)
    block_number = Column(Numeric(), nullable=False)
    bot_address = Column(String(42), nullable=True)
    pool_address = Column(String(42), nullable=False)
    token0_address = Column(String(42), nullable=True)
    token1_address = Column(String(42), nullable=True)
    mint_transaction_hash = Column(String(66), nullable=False)
    mint_transaction_trace = Column(ARRAY(Integer))
    burn_transaction_hash = Column(String(66), nullable=False)
    burn_transaction_trace = Column(ARRAY(Integer))
    mint_token0_amount = Column(Numeric)
    mint_token1_amount = Column(Numeric)
    burn_token0_amount = Column(Numeric)
    burn_token1_amount = Column(Numeric)
    token0_swap_volume = Column(Numeric)
    token1_swap_volume = Column(Numeric)



