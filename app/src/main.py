from fastapi import FastAPI
from app.src.admin.router import admin
from app.src.guest.router import guest

app = FastAPI(title="Restaurant order taker")

app.include_router(admin, tags=["admin"])
app.include_router(guest, tags=["guest"])


@app.on_event("startup")
async def startup():
    # asyncio.create_task(check_async_connections())
    # connect to db
    pass


@app.get("/", tags=["main page"])
async def root():
    return "Restaurant order taker"
