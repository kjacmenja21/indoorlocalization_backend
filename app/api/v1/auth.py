from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth.token import Token

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.get("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = None  # authenticate_user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = None  # create_access_token
    return Token()
