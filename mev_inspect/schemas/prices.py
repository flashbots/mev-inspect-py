from pydantic import BaseModel


class Price(BaseModel):
    token_address: str
    timestamp_seconds: int
    usd_price: float
