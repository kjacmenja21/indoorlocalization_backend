from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.dependancies import UserServiceDep
from app.functions.exceptions import unauthorized_bearer
from app.schemas.auth.token import Token

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login")
def login(
    user_service: UserServiceDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise unauthorized_bearer()
    access_token = None  # create_access_token
    return Token()
