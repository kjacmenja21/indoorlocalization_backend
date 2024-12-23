from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import UserServiceDep, check_refresh_token_cookie
from app.config import GeneralConfig
from app.functions.exceptions import unauthorized, unauthorized_bearer
from app.schemas.api.user import UserModelIndentified
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

    token = generate_token(response, user)

    return token


@auth_router.post("/autologin")
async def refresh_token(
    response: Response,
    user_service: UserServiceDep,
    refresh_tkn: str = Depends(check_refresh_token_cookie),
) -> TokenEncode:
    if not refresh_tkn:
        raise unauthorized("No refresh token")

    decoded_token = Token.decode_refresh(
        refresh_tkn, GeneralConfig().jwt_refresh_token_secret_key
    )
    if not decoded_token:
        raise unauthorized("Invalid refresh token")

    user = user_service.get_user(user=decoded_token.client_id)
    if not user:
        raise unauthorized("User does not exist")

    token = generate_token(response, user)

    return token


def generate_token(response: Response, user: UserModelIndentified):
    data = TokenData.model_validate(user)
    data.scope = [user.role.name]
    refresh_data = RefreshTokenData(client_id=user.id)

    token = Token(
        expires_in=GeneralConfig().jwt_access_token_expire_minutes,
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
