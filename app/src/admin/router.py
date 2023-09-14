from fastapi import APIRouter

from app.src.admin.service import AdminService

admin = APIRouter(prefix="/admin")


@admin.get("/orders")
async def get_orders():
    return await AdminService.get_orders()


# GET /orders/<id> - get a single order with items
@admin.get("/orders/{id}")
async def get_order(id: int):
    return await AdminService.get_order(id)


# DELETE /orders/<id> - delete existing order
@admin.delete("/orders/{id}")
async def del_order(id: int):
    return await AdminService.del_order(id)


# GET /order_items - return order_items table
@admin.get("/order_items")
async def get_order_items():
    return await AdminService.get_order_items()


# GET /stats - return general stats
@admin.get("/stats")
async def get_stats():
    return await AdminService.get_stats()
