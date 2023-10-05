from app.src.admin.models import Menu_item
from app.src.database import get_async_pool
from psycopg import sql

async_pool = get_async_pool()


class AdminUtils:
    @staticmethod
    async def get_completed_orders_info():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL(
                "SELECT "
                "   o.id, "
                "   total_price, "
                "   JSON_AGG( "
                "       JSONB_BUILD_OBJECT( "
                "           'name', m.name, "
                "           'number', oi.number_of_items "
                "       ) ORDER BY m.name "
                "   ) AS items, "
                "   (SELECT JSON_AGG(c.message) FROM chats c WHERE c.order_id = o.id) AS chat "
                "FROM orders o "
                "LEFT JOIN order_items oi ON o.id = oi.order_id "
                "LEFT JOIN menu m ON oi.menu_item_id = m.id "
                "WHERE o.status = 6 "
                "GROUP BY o.id, total_price "
                "ORDER BY o.id;"
            )

            await cur.execute(query)
            return await AdminUtils.parse_result(cur)

    @staticmethod
    async def get_general_stats():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL(
                "SELECT "
                "    COUNT(*) AS total_orders, "
                "    SUM(total_price) AS total_revenue, "
                "    AVG(total_price) AS average_order_price "
                "FROM orders "
                "WHERE status = 6;"
            )

            await cur.execute(query)
            result = (await AdminUtils.parse_result(cur))[0]
            query = sql.SQL(
                "SELECT "
                "   JSON_AGG( "
                "       JSONB_BUILD_OBJECT( "
                "           'name', m.name, "
                "           'number', m.number_of_orders "
                "       ) ORDER BY m.name "
                "   ) AS items "
                "FROM menu m;"
            )

            await cur.execute(query)
            result.update((await AdminUtils.parse_result(cur))[0])

            query = sql.SQL(
                "SELECT "
                "    SUM(asked) AS asked, "
                "    SUM(accepted) AS accepted, "
                "    SUM(rejected) AS rejected, "
                "    SUM(total_revenue) AS total_upsell_revenue "
                "FROM "
                "    upsell_stats;"
            )

            await cur.execute(query)
            result.update({"upsell_stats": (await AdminUtils.parse_result(cur))[0]})

            return result

    @staticmethod
    async def parse_result(cur):
        result = []
        for row in await cur.fetchall():
            row_dict = {}
            for i, column_name in enumerate(cur.description):
                row_dict[column_name[0]] = row[i]
            result.append(row_dict)
        return result

    @staticmethod
    async def add_menu_item(item: Menu_item):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL(
                "INSERT INTO "
                "menu (name, type, price, in_stock) "
                "VALUES "
                "(%s, %s, %s, %s) "
                "RETURNING id;"
            )

            data = (item.name, item.type, item.price, item.in_stock)
            await cur.execute(query, data)
            return (await AdminUtils.parse_result(cur))[0]

    @staticmethod
    async def change_stock(item_id: int, in_stock: int):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL(
                "UPDATE menu "
                "SET in_stock = %s "
                "WHERE id = %s "
                "RETURNING in_stock;"
            )

            data = (in_stock, item_id)
            await cur.execute(query, data)
            return (await AdminUtils.parse_result(cur))[0]

    @staticmethod
    async def get_menu():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            query = sql.SQL("SELECT * FROM menu ")
            await cur.execute(query)
            return await AdminUtils.parse_result(cur)
