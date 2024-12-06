from datetime import UTC, datetime, timedelta

from pydantic import BaseModel, Field, computed_field

from app.config import JWTConfig
from app.functions.exceptions import forbidden, unprocessable_entity
from app.functions.jwt import create_token, decode_token
from app.schemas.auth.token_extra import (
    AccessTokenData,
    TokenDecode,
    TokenEncode,
    TokenType,
)
from app.schemas.auth.user import Role

cfg = JWTConfig()


class Token(BaseModel):
    token_type: str = "Bearer"
    scope: list[Role] = [Role.USER]
    expires_in: int
    data: AccessTokenData
    iat: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @computed_field
    def exp(self) -> datetime:
        return self.iat + timedelta(minutes=self.expires_in)

    def encode(self) -> TokenEncode:

        access_token = create_token(
            self,
            cfg.secret_key,
            timedelta(minutes=cfg.access_token_expire_minutes),
            cfg.algorithm,
        )

        refresh_token = create_token(
            BaseModel(**{"test": "data"}),
            cfg.refresh_token_secret_key,
            timedelta(minutes=cfg.refresh_token_expire_minutes),
            cfg.algorithm,
        )

        return TokenEncode(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.expires_in,
            scope=self.scope,
            data=self.data,
        )

    @classmethod
    def decode(
        cls,
        token: str,
        scope: list[Role] | None = None,
        type: TokenType = TokenType.ACCESS,
    ) -> TokenDecode:
        if type == TokenType.ACCESS:
            key = cfg

        decoded_dict = decode_token(token, key, cfg.algorithm)

        if not decoded_dict:
            raise unprocessable_entity("Token invalid")

        decoded = Token.model_validate(decoded_dict)

        if scope:
            if "admin" in decoded.scope:
                ...
            elif not all(i in decoded.scope for i in scope):
                raise forbidden(msg="Insufficient scope.")

        return TokenDecode(**decoded.model_dump())
