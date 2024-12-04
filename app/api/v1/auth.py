from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.functions.exceptions import unauthorized_bearer
from app.schemas.auth.token import Token

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = None  # authenticate_user
    if not user:
        raise unauthorized_bearer()
    access_token = None  # create_access_token
    return Token()
