from app.src.database import get_async_pool
import asyncio

async_pool = get_async_pool()

class GuestUtils:

    @staticmethod
    async def get_menu():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute("select * from menu")
            menu = await cur.fetchall()
            return menu
