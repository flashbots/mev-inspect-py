from sqlalchemy import Column, Numeric, String, ARRAY, Integer

from .base import Base


class LiquidationModel(Base):
    __tablename__ = "liquidations"

    liquidated_user = Column(String, nullable=False)
    liquidator_user = Column(String, nullable=False)
    debt_token_address = Column(String, nullable=False)
    debt_purchase_amount = Column(Numeric, nullable=False)
    received_amount = Column(Numeric, nullable=False)
    received_token_address = Column(String, nullable=False)
    protocol = Column(String, nullable=True)
    transaction_hash = Column(String, primary_key=True)
    trace_address = Column(ARRAY(Integer), primary_key=True)
    block_number = Column(Numeric, nullable=False)
