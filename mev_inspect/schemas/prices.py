from datetime import datetime

from pydantic import BaseModel


class Price(BaseModel):
    token_address: str
    timestamp: datetime
    usd_price: float
