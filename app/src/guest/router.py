from fastapi import APIRouter
from app.src.guest.service import GuestService
from app.src.models.order import Order

guest = APIRouter(prefix="/guest")

@guest.get("")
def root():
    return {"message":"Welcome to our restaurant"}


@guest.get("/menu")
async def get_menu():
    return await GuestService.get_menu()