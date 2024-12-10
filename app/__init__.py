from fastapi import FastAPI

from app.api import add_api_routers
from app.config import FastAPISettings
from app.functions.middleware import lifespan


def create_server() -> FastAPI:

    app_instance = FastAPI(lifespan=lifespan, **FastAPISettings().model_dump())
    add_api_routers(app_instance)
    return app_instance


app = create_server()
