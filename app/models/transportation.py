from pydantic import BaseModel

class Transportation(BaseModel):
    id: int
    mode: str
    capacity: int
    cost: float
