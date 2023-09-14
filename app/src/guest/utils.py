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
            order_id = (await GuestUtils.parse_result(cur))[0]["id"]
            await cur.execute(
                f"INSERT INTO chats (order_id, message) \
                VALUES ({order_id}, 'Welcome, what can I get you?') \
                RETURNING message;"
            )

            return {"order_id": order_id, "response": (await GuestUtils.parse_result(cur))[0]["message"]}


    @staticmethod
    async def add_item(session_id: int, item_id: int):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL(
                "INSERT INTO order_items (order_id, menu_item_id) "
                "VALUES (%s, %s) "
                "ON CONFLICT (order_id, menu_item_id) "
                "DO UPDATE SET number_of_items = order_items.number_of_items + 1 "
                "RETURNING number_of_items;"
            )

            data = (session_id, item_id)
            await cur.execute(query, data)

            return (await GuestUtils.parse_result(cur))[0]

    @staticmethod
    async def set_upsell(session_id: int):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL(
                "UPDATE orders "
                "SET upsell = TRUE "
                "WHERE id = %s "
                "RETURNING upsell;"
            )

            data = (session_id,)
            await cur.execute(query, data)

            return (await GuestUtils.parse_result(cur))[0]

    @staticmethod
    async def check_order_upsell(session_id: int):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL(
                "SELECT upsell"
                "FROM orders"
                "WHERE id = %s "
                "LIMIT 1;"
            )

            data = (session_id,)
            await cur.execute(query, data)

            return (await GuestUtils.parse_result(cur))[0]

    #
    @staticmethod
    async def check_item(item_name: str):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute(
                f"SELECT id \
                FROM menu \
                WHERE name = '{item_name}';"
            )
            return await GuestUtils.parse_result(cur)
    #
    @staticmethod
    async def get_upsell():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute(
                f"SELECT * \
                    FROM menu \
                    WHERE type = 'Drink' \
                    LIMIT 1;"
            )
            return (await GuestUtils.parse_result(cur))[0]
    #
    @staticmethod
    async def parse_result(cur):
        result = []
        for row in await cur.fetchall():
            row_dict = {}
            for i, column_name in enumerate(cur.description):
                row_dict[column_name[0]] = row[i]
            result.append(row_dict)
        return result
    #
