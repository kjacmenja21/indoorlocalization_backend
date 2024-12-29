from typing import Annotated

from fastapi import Depends, Request

from app.config import GeneralConfig
from app.database.db import get_db_session
from app.database.services import UserService
from app.database.services.asset_position_service import AssetPositionService
from app.database.services.asset_service import AssetService
from app.database.services.floormap_service import FloormapService
from app.database.services.zone_service import ZoneService
from app.functions.exceptions import credentials_exception
from app.functions.schemes import oauth2_scheme
from app.schemas.api.user import UserBase
from app.schemas.auth.role_types import Role
from app.schemas.auth.token import Token


def get_user_service(session=Depends(get_db_session)) -> UserService:
    return UserService(session=session)


def get_floormap_service(session=Depends(get_db_session)) -> FloormapService:
    return FloormapService(session=session)


def get_asset_service(session=Depends(get_db_session)) -> AssetService:
    return AssetService(session=session)


def get_asset_position_service(session=Depends(get_db_session)) -> AssetPositionService:
    return AssetPositionService(session=session)


def get_zone_service(session=Depends(get_db_session)) -> ZoneService:
    return ZoneService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]

FloormapServiceDep = Annotated[FloormapService, Depends(get_floormap_service)]

AssetServiceDep = Annotated[AssetService, Depends(get_asset_service)]

AssetPositionDep = Annotated[AssetPositionService, Depends(get_asset_position_service)]

ZoneServiceDep = Annotated[ZoneService, Depends(get_zone_service)]


async def get_current_user(
    service: UserServiceDep,
    token: Annotated[str, Depends(oauth2_scheme)],
    scope: list[Role] | None = None,
) -> UserBase:
    token_decoded = Token.decode_access(
        token=token,
        scope=scope,
        key=GeneralConfig().jwt_access_token_secret_key,
    )

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


def check_refresh_token_cookie(request: Request):
    config = GeneralConfig()
    cookie = request.cookies
    if not cookie:
        return None
    if cookie.get(config.refresh_token_cookie_name):
        return cookie.get(config.refresh_token_cookie_name)
