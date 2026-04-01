from pydantic import BaseModel

class Trade(BaseModel):
    id: int
    item: str
    quantity: int
    price: float
