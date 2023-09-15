from psycopg import sql

from app.src.database import get_async_pool

async_pool = get_async_pool()


class GuestUtils:
    @staticmethod
    async def get_menu():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL("SELECT name, price FROM menu ")
            await cur.execute(query)
            return await GuestUtils.parse_result(cur)

    @staticmethod
    async def save_message(session_id: int, message: str):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL(
                "INSERT INTO chats (order_id, message) "
                "VALUES (%s, %s) "
                "RETURNING message; "
            )
            data = (session_id, message)
            await cur.execute(query, data)

            return (await GuestUtils.parse_result(cur))[0]

    @staticmethod
    async def create_order():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL("INSERT INTO orders " "DEFAULT VALUES " "RETURNING id; ")
            await cur.execute(query)
            order_id = (await GuestUtils.parse_result(cur))[0]["id"]

            query = sql.SQL(
                "INSERT INTO chats (order_id, message) "
                "VALUES (%s, %s) "
                "RETURNING message; "
            )
            data = (order_id, "Welcome, what can I get you?")
            await cur.execute(query, data)

            return {
                "order_id": order_id,
                "message": (await GuestUtils.parse_result(cur))[0]["message"],
            }

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
    async def remove_item(session_id: int, item_id: int):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query_insert = sql.SQL(
                "INSERT INTO order_items (order_id, menu_item_id) "
                "VALUES (%s, %s) "
                "ON CONFLICT (order_id, menu_item_id) "
                "DO UPDATE SET number_of_items = GREATEST(order_items.number_of_items - 1, 0) "
                "RETURNING number_of_items;"
            )

            query_delete = sql.SQL(
                "DELETE FROM order_items "
                "WHERE order_id = %s AND menu_item_id = %s "
                "RETURNING number_of_items;"
            )

            data = (session_id, item_id)
            await cur.execute(query_insert, data)
            result = await GuestUtils.parse_result(cur)

            if result and result[0]["number_of_items"] == 0:
                # If the number_of_items is 0, remove the entry from the table
                await cur.execute(query_delete, data)
                result = await GuestUtils.parse_result(cur)

            return result[0] if result else None

    @staticmethod
    async def set_upsell(session_id: int):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL(
                "UPDATE orders "
                "SET upsell = true "
                "WHERE id = %s "
                "RETURNING upsell;"
            )
            data = (session_id,)
            await cur.execute(query, data)
            return (await GuestUtils.parse_result(cur))[0]

    @staticmethod
    async def set_completed(session_id: int):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL(
                "UPDATE orders " "SET completed = true " "WHERE id = %s " "RETURNING *;"
            )
            data = (session_id,)
            await cur.execute(query, data)
            return (await GuestUtils.parse_result(cur))[0]

    @staticmethod
    async def check_order_upsell(session_id: int):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL("SELECT upsell " "FROM orders " "WHERE id = %s " "LIMIT 1;")
            data = (session_id,)
            await cur.execute(query, data)

            return (await GuestUtils.parse_result(cur))[0]

    @staticmethod
    async def check_item(item_name: str):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL("SELECT id " "FROM menu " "WHERE name = %s " "LIMIT 1;")
            data = (item_name,)
            await cur.execute(query, data)

            return (await GuestUtils.parse_result(cur))[0]

    @staticmethod
    async def get_upsell():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL("SELECT * " "FROM menu " "WHERE type = %s " "LIMIT 1;")
            data = ("Drink",)
            await cur.execute(query, data)

            return (await GuestUtils.parse_result(cur))[0]

    @staticmethod
    async def accept_upsell():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL(
                "INSERT INTO upsell_stats (upsell_id) "
                "VALUES (%s) "
                "ON CONFLICT (upsell_id) DO UPDATE "
                "SET accepted = upsell_stats.accepted + 1 "
                "RETURNING accepted;"
            )

            data = ((await GuestUtils.get_upsell())["id"],)
            await cur.execute(query, data)

            return await GuestUtils.parse_result(cur)

    @staticmethod
    async def ask_upsell():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL(
                "INSERT INTO upsell_stats (upsell_id) "
                "VALUES (%s) "
                "ON CONFLICT (upsell_id) DO UPDATE "
                "SET asked = upsell_stats.asked + 1 "
                "RETURNING asked;"
            )

            data = ((await GuestUtils.get_upsell())["id"],)
            await cur.execute(query, data)

            return await GuestUtils.parse_result(cur)

    @staticmethod
    async def reject_upsell():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL(
                "INSERT INTO upsell_stats (upsell_id) "
                "VALUES (%s) "
                "ON CONFLICT (upsell_id) DO UPDATE "
                "SET rejected = upsell_stats.rejected + 1 "
                "RETURNING rejected;"
            )

            data = ((await GuestUtils.get_upsell())["id"],)
            await cur.execute(query, data)

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
