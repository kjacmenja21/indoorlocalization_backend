from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.v1.dependancies import UserServiceDep, get_current_user_with_scope
from app.functions.exceptions import unprocessable_entity
from app.functions.schemes import oauth2_scheme
from app.schemas.api.user import UserCreate, UserModel
from app.schemas.auth.token import Token
from app.schemas.auth.user import Role

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get("/")
async def get_all_users(
    user_service: UserServiceDep,
    user: UserModel = get_current_user_with_scope([Role.ADMIN]),
) -> list[UserModel]:
    return user_service.get_all_users()


@user_router.post("/")
def user_create(
    user: UserCreate,
    user_service: UserServiceDep,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    decoded = Token.decode(token=token, scope=[Role.ADMIN])
    new_user = user_service.create_user(user)
    if not new_user:
        raise unprocessable_entity()

    return JSONResponse(
        {
            "message": "User successfully created.",
            "user": new_user.model_dump(exclude=["salt", "password"]),
        }
    )
