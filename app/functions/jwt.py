import datetime
from datetime import datetime as dt
from datetime import timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.config import JWTConfig

# Secret key to encode and decode JWT
config = JWTConfig()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_access_token(data: BaseModel, expires_delta: timedelta | None = None) -> str:

    to_encode = data.model_dump()

    if expires_delta:
        expire = dt.now(datetime.timezone.utc) + expires_delta
    else:
        expire = dt.now(datetime.timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        return payload
    except JWTError:
        return None
