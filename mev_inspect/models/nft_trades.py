from sqlalchemy import ARRAY, Column, Integer, Numeric, String

from .base import Base


class NftTradeModel(Base):
    __tablename__ = "nft_trades"

    abi_name = Column(String, nullable=False)
    transaction_hash = Column(String, primary_key=True)
    transaction_position = Column(Numeric, nullable=True)
    block_number = Column(Numeric, nullable=False)
    trace_address = Column(ARRAY(Integer), primary_key=True)
    protocol = Column(String, nullable=True)
    error = Column(String, nullable=True)
    seller_address = Column(String, nullable=False)
    buyer_address = Column(String, nullable=False)
    payment_token_address = Column(String, nullable=False)
    payment_amount = Column(Numeric, nullable=False)
    collection_address = Column(String, nullable=False)
    token_id = Column(Numeric, nullable=False)
