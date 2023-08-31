from app.src.database import get_async_pool

async_pool = get_async_pool()


class AdminUtils:
    @staticmethod
    async def get_orders():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute("select * from orders")
            return await cur.fetchall()

    @staticmethod
    async def get_order(id: int):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute(
                f"SELECT \
                o.id AS order_id, \
                o.time_created AS order_time, \
                o.total_price AS order_total_price, \
                o.number_of_all_items AS order_total_items, \
                mi.id AS menu_item_id, \
                mi.name AS menu_item_name, \
                mi.type AS menu_item_type, \
                mi.price AS menu_item_price, \
                oi.number_of_items AS item_quantity \
            FROM \
                orders o \
            JOIN \
                order_items oi ON o.id = oi.order_id \
            JOIN \
                menu mi ON oi.menu_item_id = mi.id \
            WHERE \
                o.id = {id}; \
            "
            )
            return await cur.fetchall()

    @staticmethod
    async def del_order(id: int):
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute(f"DELETE FROM orders \
                                WHERE id = {id};")
            return 200

    @staticmethod
    async def get_order_items():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute("select * from order_items")
            return await cur.fetchall()

    @staticmethod
    async def get_stats():
        async with async_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute("SELECT \
                    COUNT(*) AS total_orders, \
                    SUM(total_price) AS total_revenue, \
                    AVG(total_price) AS average_order_price, \
                    MIN(total_price) AS min_order_price, \
                    MAX(total_price) AS max_order_price, \
                    AVG(number_of_all_items) AS average_items_per_order, \
                    MIN(number_of_all_items) AS min_items_per_order, \
                    MAX(number_of_all_items) AS max_items_per_order \
                FROM \
                    orders;")
            return await cur.fetchall()


