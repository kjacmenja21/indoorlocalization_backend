from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.dependancies import UserServiceDep
from app.config import JWTConfig
from app.functions.exceptions import unauthorized_bearer
from app.schemas.auth.token import Token
from app.schemas.auth.token_extra import AccessTokenData, TokenEncode

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login", response_model_exclude_none=True)
def login(
    user_service: UserServiceDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> TokenEncode:
    user = user_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise unauthorized_bearer()

    data = AccessTokenData.model_validate(user)

    return Token(
        expires_in=JWTConfig().access_token_expire_minutes,
        data=data,
        scope=[user.role.name],
    ).encode()
