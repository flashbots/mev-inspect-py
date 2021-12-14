from sqlalchemy import TIMESTAMP, Column, Numeric, String

from .base import Base


class PriceModel(Base):
    __tablename__ = "prices"

    timestamp = Column(TIMESTAMP, nullable=False, primary_key=True)
    usd_price = Column(Numeric, nullable=False)
    token_address = Column(String, nullable=False, primary_key=True)
