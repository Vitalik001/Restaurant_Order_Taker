from pydantic import BaseModel


class Order(BaseModel):
    id: int
    time_created: str
    total_price: float


