from app.src.admin.utils import AdminUtils


class AdminService:
    @staticmethod
    async def get_orders():
        return await AdminUtils.get_orders()

    @staticmethod
    async def get_order(id: int):
        return await AdminUtils.get_order(id)

    @staticmethod
    async def del_order(id: int):
        return await AdminUtils.del_order(id)


    @staticmethod
    async def get_order_items():
        return await AdminUtils.get_order_items()

    @staticmethod
    async def get_stats():
        return await AdminUtils.get_stats()