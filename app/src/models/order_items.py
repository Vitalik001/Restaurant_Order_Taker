from pydantic import BaseModel


class OrderItems(BaseModel):
    order_id: int
    menu_item_id: int
