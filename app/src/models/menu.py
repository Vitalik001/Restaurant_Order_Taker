from pydantic import BaseModel


class Menu(BaseModel):
    name: str
    type: str
    price: float
