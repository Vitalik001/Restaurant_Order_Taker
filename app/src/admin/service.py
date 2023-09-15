from app.src.admin.utils import AdminUtils


class AdminService:
    @staticmethod
    async def get_completed_orders_info():
        return await AdminUtils.get_completed_orders_info()

    @staticmethod
    async def get_general_stats():
        return await AdminUtils.get_general_stats()
