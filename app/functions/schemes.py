from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.functions.exceptions import credentials_exception
from app.schemas.auth.token import Token
from app.schemas.auth.user import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")
