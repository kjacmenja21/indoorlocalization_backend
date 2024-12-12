import logging
from datetime import UTC
from datetime import datetime as dt
from datetime import timedelta
from typing import Any, Optional

import bcrypt
from jose import JWTError, jwt
from pydantic import BaseModel, SecretStr

logger = logging.getLogger(__name__)


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        bytes(plain_password, encoding="utf-8"),
        hashed_password,
    )


def get_password_hash(
    password: str | SecretStr, salt: Optional[bytes]
) -> tuple[bytes, bytes]:
    if isinstance(password, SecretStr):
        password = password.get_secret_value()
    if salt is None:
        salt = generate_salt()
    return (bcrypt.hashpw(bytes(password, encoding="utf-8"), salt), salt)


def generate_salt() -> bytes:
    return bcrypt.gensalt()


def create_token(
    data: BaseModel,
    key: str,
    expires_delta: timedelta = timedelta(minutes=30),
    algorithm: str = "HS256",
) -> str:
    to_encode = data.model_dump(exclude_none=True)

    expire = dt.now(UTC) + expires_delta
    to_encode.update({"exp": expire})

    try:
        encoded_jwt = jwt.encode(to_encode, key=key, algorithm=algorithm)
        return encoded_jwt
    except JWTError as e:
        logger.error(e)


def decode_token(
    token: str, key: str, algorithm: str = "HS256"
) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(token, key=key, algorithms=[algorithm])
        return payload
    except JWTError:
        return None
