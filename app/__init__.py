from typing import Callable, Type

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.api import add_api_routers
from app.config import FastAPISettings
from app.functions.middleware import lifespan


class MiddlewareItem(BaseModel):
    middleware_class: Type
    config: dict


def create_server(
    lifespan_function: Callable[[FastAPI], None], middleware_list: list[MiddlewareItem]
) -> FastAPI:
    app_instance = FastAPI(lifespan=lifespan_function, **FastAPISettings().model_dump())

    for item in middleware_list:
        app_instance.add_middleware(
            item.middleware_class,
            **item.config,
        )

    add_api_routers(app_instance)
    return app_instance


middlewares = [
    MiddlewareItem(
        middleware_class=CORSMiddleware,
        config={
            "allow_origins": ["*"],
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        },
    )
]

app = create_server(lifespan, middlewares)
