from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from app.api.v1.dependancies import UserServiceDep, get_current_user_with_scope
from app.functions.exceptions import unprocessable_entity
from app.functions.schemes import oauth2_scheme
from app.schemas.api.user import UserCreate, UserModel
from app.schemas.auth.token import Token
from app.schemas.auth.token_extra import TokenType
from app.schemas.auth.user import Role

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get("/")
async def get_all_users(
    user_service: UserServiceDep,
    _: UserModel = get_current_user_with_scope([Role.ADMIN]),
) -> list[UserModel]:
    users = user_service.get_all_users()

    return [user.model_dump() for user in users]


@user_router.post("/")
def user_create(
    user_service: UserServiceDep,
    token: Annotated[str, Depends(oauth2_scheme)],
    user: UserCreate = Query(UserCreate),
) -> JSONResponse:
    decoded = Token.decode(token=token, scope=[Role.ADMIN], type=TokenType.ACCESS)
    new_user = user_service.create_user(user)
    if not new_user:
        raise unprocessable_entity()

    return JSONResponse(
        {
            "message": "User successfully created.",
            "user": new_user,
        }
    )
