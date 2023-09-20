from pydantic import BaseModel

class Menu_item(BaseModel):
    name: str
    type: str
    price: float
    in_stock: int

class Item(BaseModel):
    id: int
    name: str
    type: str
    price: float
    in_stock: int