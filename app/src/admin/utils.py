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
                "WHERE o.completed = true "
                "GROUP BY o.id, total_price "
                "ORDER BY o.id;"
            )

            await cur.execute(query)
            return await AdminUtils.parse_result(cur)

    async def get_order(id: int):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute(
                f"SELECT * from orders where id = {id}"
            )
            return await cur.fetchall()

    @staticmethod
    async def del_order(id: int):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute(
                f"DELETE FROM orders \
                                WHERE id = {id};"
            )
            return 200

    @staticmethod
    async def get_order_items():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute("select * from order_items")
            return await cur.fetchall()

    @staticmethod
    async def get_stats():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute(
                "SELECT \
                    COUNT(*) AS total_orders, \
                    SUM(total_price) AS total_revenue, \
                    AVG(total_price) AS average_order_price, \
                    MIN(total_price) AS min_order_price, \
                    MAX(total_price) AS max_order_price, \
                    AVG(number_of_all_items) AS average_items_per_order, \
                    MIN(number_of_all_items) AS min_items_per_order, \
                    MAX(number_of_all_items) AS max_items_per_order \
                FROM \
                    orders;"
            )
            return await cur.fetchall()

    @staticmethod
    async def parse_result(cur):
        result = []
        for row in await cur.fetchall():
            row_dict = {}
            for i, column_name in enumerate(cur.description):
                row_dict[column_name[0]] = row[i]
            result.append(row_dict)
        return result
