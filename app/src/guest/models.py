from typing import List

from pydantic import BaseModel


class Create_order_responce(BaseModel):
    order_id: int
    message: str


class Menu_item(BaseModel):
    name: str
    price: float


class Message_responce(BaseModel):
    message: str
