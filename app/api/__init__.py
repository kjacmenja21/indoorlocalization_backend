from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse

redirect_router = APIRouter()
api_router = APIRouter(prefix="/api")

from app.api.v1 import v1_router

api_router.include_router(v1_router)


@redirect_router.get("/", include_in_schema=False)
async def docs_redirect() -> RedirectResponse:
    return RedirectResponse(url="/docs")


def add_api_routers(app: FastAPI):
    app.include_router(router=api_router)
    app.include_router(router=redirect_router)
