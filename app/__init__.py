from fastapi import FastAPI

from app.api import add_api_routers
from app.config import FastAPISettings
from app.functions.middleware import lifespan


def create_server() -> FastAPI:
    app = FastAPI(lifespan=lifespan, **FastAPISettings().model_dump())
    add_api_routers(app)
    return app


app = create_server()
