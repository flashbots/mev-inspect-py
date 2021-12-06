from sqlalchemy import Column, Numeric, String, TIMESTAMP

from .base import Base


class PriceModel(Base):
    __tablename__ = "prices"

    timestamp = Column(TIMESTAMP, nullable=False, primary_key=True)
    usd_price = Column(Numeric, nullable=False)
    token_address = Column(String, nullable=False, primary_key=True)
