from calendar import c

import pytest
from fastapi import HTTPException

from app.config import GeneralConfig
from app.functions.exceptions import forbidden, unprocessable_entity
from app.functions.jwt_functions import create_token
from app.schemas.api.user import UserRoleModel
from app.schemas.auth.role_types import Role
from app.schemas.auth.token import Token
from app.schemas.auth.token_extra import (
    RefreshTokenData,
    TokenData,
    TokenDecode,
    TokenEncode,
)


@pytest.fixture
def token_data() -> TokenData:
    return TokenData(
        id=1,
        username="testuser",
        email="testuser@example.com",
        first_name="Test",
        last_name="User",
        contact="1234567890",
        role=UserRoleModel(id=1, name=Role.USER),
    )


@pytest.fixture
def refresh_token_data() -> RefreshTokenData:
    return RefreshTokenData(
        user_id=1,
        username="testuser",
        client_id=1,
    )


@pytest.fixture
def token(token_data, refresh_token_data) -> Token:
    return Token(
        expires_in=15,
        data=token_data,
        refresh_data=refresh_token_data,
        scope=[Role.USER],
    )


def test_encode(token: Token):
    encoded = token.encode()
    assert isinstance(encoded, TokenEncode)
    assert encoded.access_token is not None
    assert encoded.expires_in == token.expires_in


def test_decode_refresh(token: Token, refresh_token_data: RefreshTokenData):
    refresh_token = create_token(
        refresh_token_data, GeneralConfig().jwt_refresh_token_secret_key
    )
    decoded = Token.decode_refresh(
        refresh_token, GeneralConfig().jwt_refresh_token_secret_key
    )
    assert isinstance(decoded, RefreshTokenData)


def test_decode_refresh_invalid_token():
    with pytest.raises(HTTPException):
        Token.decode_refresh(
            "invalid_token", GeneralConfig().jwt_refresh_token_secret_key
        )


def test_decode_access(token: Token, token_data: TokenData):
    access_token = create_token(token_data, GeneralConfig().jwt_access_token_secret_key)
    decoded = Token.decode_access(
        access_token, GeneralConfig().jwt_access_token_secret_key
    )
    assert isinstance(decoded, TokenDecode)
    assert decoded.username == token_data.username


def test_decode_access_invalid_token():
    with pytest.raises(HTTPException):
        Token.decode_access(
            "invalid_token", GeneralConfig().jwt_access_token_secret_key
        )


def test_decode_access_insufficient_scope(token: Token, token_data: TokenData):
    access_token = create_token(token_data, GeneralConfig().jwt_access_token_secret_key)
    with pytest.raises(HTTPException):
        Token.decode_access(
            access_token,
            GeneralConfig().jwt_access_token_secret_key,
            scope=[Role.ADMIN],
        )
