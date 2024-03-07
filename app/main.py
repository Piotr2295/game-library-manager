from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import HTMLResponse

from app.routers.auth import router as login_router
from app.routers.registration import router as registration_router
from app.routers.games import router as games_router

app = FastAPI()
app.include_router(registration_router)
app.include_router(games_router)
app.include_router(login_router)


@app.get("/docs", response_class=HTMLResponse)
async def get_swagger_ui():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Swagger UI")


@app.get("/")
async def root():
    return {"message": "Welcome to your game library!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
