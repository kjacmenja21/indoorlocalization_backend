from fastapi import APIRouter, FastAPI

router = APIRouter(prefix="/api")

from app.api.v1 import v1_router

router.include_router(v1_router)


def add_api_routers(app: FastAPI):
    app.include_router(router=router)
