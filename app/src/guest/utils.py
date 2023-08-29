from app.src.database import get_async_pool
from app.src.models.item import Item

async_pool = get_async_pool()


class GuestUtils:
    @staticmethod
    async def get_menu():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute("select * from menu")
            return await cur.fetchall()

    @staticmethod
    async def create_order():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO orders (time_created) \
                                VALUES (CURRENT_TIMESTAMP) \
                                RETURNING id;"
            )
            return await cur.fetchall()

    @staticmethod
    async def add_item(order_id: int, item: Item):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute(
                f"INSERT INTO order_items (order_id, menu_item_id, number_of_items) \
                                        VALUES \
                                        ({order_id}, {item.item_id}, {item.number_of_items})"
            )
