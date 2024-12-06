from typing import Annotated

from fastapi import Depends

from app.database.db import get_db_session
from app.database.services import UserService
from app.functions.exceptions import credentials_exception
from app.functions.schemes import oauth2_scheme
from app.schemas.api.user import UserBase
from app.schemas.auth.token import Token
from app.schemas.auth.user import Role


def get_user_service(session=Depends(get_db_session)) -> UserService:
    return UserService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_current_user(
    service: UserServiceDep,
    token: Annotated[str, Depends(oauth2_scheme)],
    scope: list[Role] | None = None,
) -> UserBase:
    token_decoded = Token.decode(token=token, scope=scope)

    user = UserBase(**token_decoded.model_dump())

    user_exists = service.user_exists(user)
    if user_exists is False:
        raise credentials_exception()

    return user


def get_current_user_with_scope(scope: list[Role]) -> UserBase:
    async def dependency(
        service: UserServiceDep,
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> UserBase:
        return await get_current_user(service, token, scope=scope)

    return Depends(dependency)
