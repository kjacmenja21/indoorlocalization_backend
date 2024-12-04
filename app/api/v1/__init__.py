from fastapi import APIRouter

from app.api.v1.auth import auth_router
from app.api.v1.test_file import test_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(test_router)
v1_router.include_router(auth_router)
