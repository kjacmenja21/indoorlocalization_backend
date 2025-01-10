from typing import Callable

from fastapi import FastAPI

from app.api import add_api_routers
from app.config import FastAPISettings
from app.functions.middleware import lifespan


def create_server(lifespan_function: Callable[[FastAPI], None]) -> FastAPI:
    app_instance = FastAPI(lifespan=lifespan_function, **FastAPISettings().model_dump())
    add_api_routers(app_instance)
    return app_instance


app = create_server(lifespan)
