from typing import List

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
async def create_order(items: List[Item]):
    order_id = (await GuestService.create_order())[0]["id"]
    for item in items:
        await GuestService.add_item(order_id, item)
    return order_id


@guest.post("/order/{order_id}/item")
async def add_item(order_id: int, item: Item):
    return await GuestService.add_item(order_id, item)

@guest.get("/check_item")
async def check_item(item_name: str):
    return await GuestService.check_item(item_name)

@guest.get("/upsell")
async def get_upsell_id():
        return await GuestService.get_upsell()
