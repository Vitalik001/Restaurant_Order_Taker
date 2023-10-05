from typing import List

from fastapi import APIRouter

from app.src.guest.models import Menu_item, Create_order_responce, Message_responce
from app.src.guest.service import GuestService


guest = APIRouter(prefix="/guest")


@guest.get("", response_model=Message_responce)
def root():
    return {"message": "Welcome to our restaurant"}


@guest.get("/menu", response_model=List[Menu_item])
async def get_menu():
    return await GuestService.get_menu()


@guest.post("/create_session", response_model=Create_order_responce)
async def create_session():
    return await GuestService.create_order()


@guest.post("/send_message/{session_id}", response_model=Message_responce)
async def handle_message(session_id: int, message: str):
    return await GuestService.handle_message(session_id, message)
