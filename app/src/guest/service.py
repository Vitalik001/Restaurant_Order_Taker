from app.src.guest.utils import GuestUtils


class GuestService:

    @staticmethod
    async def get_menu():
        return await GuestUtils.get_menu()
