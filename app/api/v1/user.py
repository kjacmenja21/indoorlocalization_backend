from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.v1.dependancies import UserServiceDep
from app.functions.exceptions import unprocessable_entity
from app.functions.schemes import oauth2_scheme
from app.schemas.api.user import UserCreate, UserModel

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get("/")
async def get_all_users(
    user_service: UserServiceDep, token: Annotated[str, Depends(oauth2_scheme)]
) -> list[UserModel]:
    return user_service.get_all_users()


@user_router.post("/")
def user_create(user: UserCreate, user_service: UserServiceDep) -> None:
    new_user = user_service.create_user(user)
    if not new_user:
        raise unprocessable_entity()
