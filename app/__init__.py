from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import add_api_routers
from app.config import FastAPISettings
from app.functions.middleware import lifespan


def create_server() -> FastAPI:
    origins = ["*"]
    app_instance = FastAPI(lifespan=lifespan, **FastAPISettings().model_dump())

    print("\nadd_middleware\nTODO: Update origins to not be '*' (other allow_*'s too)")
    app_instance.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_api_routers(app_instance)
    return app_instance


app = create_server()
