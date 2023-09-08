from typing import List

from psycopg import sql

from app.src.database import get_async_pool
from app.src.models.item import Item
async_pool = get_async_pool()


class GuestUtils:
    @staticmethod
    async def get_menu():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute("select * from menu")
            return await GuestUtils.parse_result(cur)

    @staticmethod
    async def create_order():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO orders (time_created) \
                                VALUES (CURRENT_TIMESTAMP) \
                                RETURNING id;"
            )
            return await GuestUtils.parse_result(cur)


    @staticmethod
    async def add_items(order_id: int, items: List[Item]):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL(
                "INSERT INTO order_items (order_id, menu_item_id, number_of_items) "
                "VALUES (%s, %s, %s)")
            for item in items:
                data = (order_id, item.item_id, item.number_of_items)
                await cur.execute(query, data)
            await cur.execute(
                f"SELECT * \
                            FROM orders \
                            WHERE id = '{order_id}';"
            )
            return await GuestUtils.parse_result(cur)


    @staticmethod
    async def check_item(item_name: str):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute(
                f"SELECT id \
                FROM menu \
                WHERE name = '{item_name}';"
            )
            return await GuestUtils.parse_result(cur)

    @staticmethod
    async def get_upsell():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute(
                f"SELECT * \
                    FROM menu \
                    WHERE type = 'Drink' \
                    LIMIT 1;"
            )
            return await GuestUtils.parse_result(cur)

    @staticmethod
    async def parse_result(cur):
        result = []
        for row in await cur.fetchall():
            row_dict = {}
            for i, column_name in enumerate(cur.description):
                row_dict[column_name[0]] = row[i]
            result.append(row_dict)
        return result

