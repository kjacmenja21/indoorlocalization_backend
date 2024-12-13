from fastapi import APIRouter

from app.api.v1.auth import auth_router
from app.api.v1.floormaps import floormap_router
from app.api.v1.users import user_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth_router)
v1_router.include_router(user_router)
v1_router.include_router(floormap_router)
