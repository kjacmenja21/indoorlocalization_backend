from fastapi import APIRouter

from app.api.v1.dependancies import UserServiceDep
from app.functions.exceptions import unprocessable_entity
from app.schemas.api.user import UserCreate

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("/")
def user_create(
    user: UserCreate,
    user_service: UserServiceDep,
):
    new_user = user_service.create_user(user)
    if not new_user:
        raise unprocessable_entity()
