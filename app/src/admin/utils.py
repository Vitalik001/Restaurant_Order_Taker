from app.src.guest.utils import async_pool


class AdminUtils:
    @staticmethod
    async def get_orders():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute("select * from orders")
            return await cur.fetchall()
