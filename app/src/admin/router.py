from fastapi import APIRouter

from app.src.admin.service import AdminService

admin = APIRouter(prefix="/admin")


@admin.get("/orders")
async def get_orders():
    return await AdminService.get_orders()


# GET /orders/<id> - get a single order with items
# DELETE /orders/<id> - delete existing order
# GET /stats - return general stats
