from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependancies import UserServiceDep
from app.config import GeneralConfig, JWTConfig
from app.functions.exceptions import unauthorized_bearer
from app.schemas.auth.token import Token
from app.schemas.auth.token_extra import RefreshTokenData, TokenData, TokenEncode

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login", response_model_exclude_none=True)
def login(
    response: Response,
    user_service: UserServiceDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> TokenEncode:
    user = user_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise unauthorized_bearer()

    data = TokenData.model_validate(user)
    data.scope = [user.role.name]
    refresh_data = RefreshTokenData(client_id=user.id)

    token = Token(
        expires_in=JWTConfig().access_token_expire_minutes,
        data=data,
        refresh_data=refresh_data,
        scope=data.scope,
    ).encode()

    response.set_cookie(
        key=GeneralConfig().refresh_token_cookie_name,
        value=token.refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    return token
