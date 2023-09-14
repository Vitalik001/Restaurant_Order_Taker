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


# @guest.post("/order")
# async def create_order(items: List[Item]):
#     order_id = (await GuestService.create_order())[0]["id"]
#     return await add_items(order_id, items)


# @guest.post("/order/{order_id}/item")
# async def add_items(order_id: int, items: List[Item]):
#     return await GuestService.add_items(order_id, items)
#
# @guest.get("/check_item")
# async def check_item(item_name: str):
#     return await GuestService.check_item(item_name)
#
@guest.get("/upsell")
async def get_upsell_id():
        return await GuestService.get_upsell()

# returns session id which is id of created order
@guest.post("/create_session")
async def create_session():
    return await GuestService.create_order()

@guest.post("/send_message/{session_id}")
async def handle_message(session_id: int, message: str):
    return await GuestService.handle_message(session_id, message)