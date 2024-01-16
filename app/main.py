from fastapi import FastAPI

from app.routers.auth import router as login_router
from app.routers.registration import router as registration_router
from app.routers.games import router as games_router


app = FastAPI()
app.include_router(registration_router)
app.include_router(games_router)
app.include_router(login_router)


@app.get("/")
async def root():
    return {"message": "Welcome to your game library!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}