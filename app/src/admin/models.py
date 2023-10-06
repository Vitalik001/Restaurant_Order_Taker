from typing import List, Optional

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


class Order_item(BaseModel):
    name: Optional[str]
    number: Optional[int]


class Order_stats(BaseModel):
    id: int
    total_price: float
    items: List[Order_item]
    chat: List[str]


class Upsell_stats(BaseModel):
    asked: int
    accepted: int
    rejected: int
    total_upsell_revenue: float


class General_stats(BaseModel):
    total_orders: int
    total_revenue: float
    average_order_price: float
    items: List[Order_item]
    upsell_stats: Upsell_stats


class Id(BaseModel):
    id: int


class In_stock(BaseModel):
    in_stock: int
