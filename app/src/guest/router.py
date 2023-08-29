from fastapi import APIRouter
from app.src.guest.service import GuestService
from app.src.models.item import Item


guest = APIRouter(prefix="/guest")


@guest.get("")
def root():
    return {"message": "Welcome to our restaurant"}


@guest.get("/menu")
async def get_menu():
    return await GuestService.get_menu()


@guest.post("/order")
async def create_order():
    return await GuestService.create_order()


@guest.post("/order/{order_id}/items")
async def add_items(order_id: int, item: Item):
    return await GuestService.add_item(order_id, item)
