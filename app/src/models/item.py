from pydantic import BaseModel


class Item(BaseModel):
    item_id: int
    number_of_items: int
