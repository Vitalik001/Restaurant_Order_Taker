from fastapi import APIRouter

from app.src.admin.service import AdminService

admin = APIRouter(prefix="/admin")


@admin.get("")
def root():
    return {"message": "You are on an admin page"}


@admin.get("/orders")
async def get_completed_orders_info():
    return await AdminService.get_completed_orders_info()


# GET /stats - return general stats
@admin.get("/stats")
async def get_general_stats():
    return await AdminService.get_general_stats()
