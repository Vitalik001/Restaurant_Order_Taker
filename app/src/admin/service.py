from app.src.admin.models import Menu_item
from app.src.admin.utils import AdminUtils


class AdminService:
    @staticmethod
    async def get_completed_orders_info():
        return await AdminUtils.get_completed_orders_info()

    @staticmethod
    async def get_general_stats():
        return await AdminUtils.get_general_stats()

    @staticmethod
    async def add_menu_item(item: Menu_item):
        return await AdminUtils.add_menu_item(item)

    @staticmethod
    async def change_stock(item_id: int, in_stock: int):
        return await AdminUtils.change_stock(item_id, in_stock)

    @staticmethod
    async def get_menu():
        return await AdminUtils.get_menu()
