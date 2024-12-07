from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.api.dependencies import UserServiceDep, get_current_user_with_scope
from app.functions.exceptions import unprocessable_entity
from app.schemas.api.user import UserBase, UserCreate, UserModel
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
    _: UserBase = get_current_user_with_scope([Role.ADMIN]),
    user: UserCreate = Query(),
) -> JSONResponse:
    new_user = user_service.create_user(user)
    if not new_user:
        raise unprocessable_entity()

    return JSONResponse(
        {
            "message": "User successfully created.",
            "user": UserModel(**new_user.model_dump()).model_dump(),
        }
    )
