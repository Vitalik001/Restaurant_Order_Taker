from typing import List

from app.src.guest.utils import GuestUtils
from app.src.models.item import Item


class GuestService:
    @staticmethod
    async def get_menu():
        return await GuestUtils.get_menu()

    @staticmethod
    async def create_order():
        return await GuestUtils.create_order()

    @staticmethod
    async def add_items(order_id: int, item: List[Item]):
        return await GuestUtils.add_items(order_id, item)

    @staticmethod
    async def check_item(item_name: str):
        return await GuestUtils.check_item(item_name)

    @staticmethod
    async def get_upsell():
        return await GuestUtils.get_upsell()

