from app.src.admin.utils import AdminUtils


class AdminService:
    @staticmethod
    async def get_orders():
        return await AdminUtils.get_orders()
