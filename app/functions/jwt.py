from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

# Secret key to encode and decode JWT


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)
