from typing import List

from app.src.guest.utils import GuestUtils
from app.src.models.item import Item
from app.src.models.order import Order

class GuestService:

    @staticmethod
    async def get_menu():
        return await GuestUtils.get_menu()

    @staticmethod
    async def create_order():
        return await GuestUtils.create_order()

    @staticmethod
    async def add_item(order_id: int, item: Item):
        return await GuestUtils.add_item(order_id, item)
