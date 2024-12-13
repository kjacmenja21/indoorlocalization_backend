from fastapi import APIRouter

from app.api.v1.assets import asset_router
from app.api.v1.auth import auth_router
from app.api.v1.user import user_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth_router)
v1_router.include_router(user_router)
v1_router.include_router(asset_router)
