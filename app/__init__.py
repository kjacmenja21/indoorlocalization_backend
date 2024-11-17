from fastapi import FastAPI

from app.api import add_api_routers
from app.config import FastAPISettings


def create_server() -> FastAPI:
    app = FastAPI(**FastAPISettings().model_dump())
    add_api_routers(app)
    return app


app = create_server()
