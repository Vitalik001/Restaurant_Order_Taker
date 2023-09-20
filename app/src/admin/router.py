from fastapi import APIRouter

from app.src.admin.models.menu_item import Menu_item
from app.src.admin.models.menu_item import Item
from app.src.admin.service import AdminService

admin = APIRouter(prefix="/admin")


@admin.get("")
def root():
    return {"message": "You are on an admin page"}


@admin.get("/orders")
async def get_completed_orders_info():
    return await AdminService.get_completed_orders_info()


@admin.get("/stats")
async def get_general_stats():
    return await AdminService.get_general_stats()

@admin.post("/add_menu_item")
async def add_menu_item(item: Menu_item):
    return await AdminService.add_menu_item(item)


@admin.put("/change_stock/{item_id}")
async def change_stock(item_id: int, in_stock: int):
    return await AdminService.change_stock(item_id, in_stock)



@admin.get("/get_menu", response_model=list[Item])
async def get_menu():
    return await AdminService.get_menu()

