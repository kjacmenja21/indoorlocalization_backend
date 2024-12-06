from datetime import UTC, datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, computed_field

from app.config import JWTConfig
from app.functions.exceptions import forbidden, unprocessable_entity
from app.functions.jwt import create_token, decode_token
from app.schemas.auth.token_extra import (
    RefreshTokenData,
    TokenData,
    TokenDecode,
    TokenEncode,
)
from app.schemas.auth.user import Role


class Token(BaseModel):
    token_type: str = "Bearer"
    scope: list[Role] = [Role.USER]
    expires_in: int
    data: TokenData
    refresh_data: Optional[RefreshTokenData] = None
    iat: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @computed_field
    def exp(self) -> datetime:
        return self.iat + timedelta(minutes=self.expires_in)

    def encode(self) -> TokenEncode:
        self.data.iat = self.iat
        self.data.exp = self.exp

        access_token = self.generate_access_token()

        refresh_token = None
        if self.refresh_data:
            refresh_token = create_token(
                self.refresh_data,
                JWTConfig().refresh_token_secret_key,
            )
        return TokenEncode(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.expires_in,
            scope=self.scope,
            data=self.data,
        )

    def generate_access_token(self) -> str:
        access_token = create_token(self.data, JWTConfig().access_token_secret_key)
        return access_token

    @classmethod
    def decode_refresh(cls, token: str, key) -> RefreshTokenData | None:
        decoded_dict = decode_token(token, key)
        if not decoded_dict:
            raise unprocessable_entity("Token invalid")

        try:
            refresh_token = RefreshTokenData.model_validate(decoded_dict)
            return refresh_token
        except ValidationError:
            return None

    @classmethod
    def decode_access(
        cls, token: str, key: str, scope: list[Role] | None = None
    ) -> TokenDecode:
        decoded_dict = decode_token(token, key)
        print(decoded_dict)
        if not decoded_dict:
            raise unprocessable_entity("Token invalid")

        decoded = TokenDecode.model_validate(decoded_dict)

        if scope:
            if Role.ADMIN in decoded.scope:
                ...
            elif not all(i in decoded.scope for i in scope):
                raise forbidden(msg="Insufficient scope.")

        return decoded
