
from fastapi import APIRouter
from app.src.guest.service import GuestService


guest = APIRouter(prefix="/guest")


@guest.get("")
def root():
    return {"message": "Welcome to our restaurant"}


@guest.get("/menu")
async def get_menu():
    return await GuestService.get_menu()

@guest.post("/create_session")
async def create_session():
    return await GuestService.create_order()

@guest.post("/send_message/{session_id}")
async def handle_message(session_id: int, message: str):
    return await GuestService.handle_message(session_id, message)