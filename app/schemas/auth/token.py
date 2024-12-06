from datetime import UTC, datetime, timedelta

from pydantic import BaseModel, Field, computed_field

from app.config import JWTConfig
from app.functions.exceptions import forbidden, unprocessable_entity
from app.functions.jwt import create_token, decode_token
from app.schemas.auth.token_extra import TokenData, TokenDecode, TokenEncode
from app.schemas.auth.user import Role


class Token(BaseModel):
    token_type: str = "Bearer"
    scope: list[Role] = [Role.USER]
    expires_in: int
    data: TokenData
    iat: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @computed_field
    def exp(self) -> datetime:
        return self.iat + timedelta(minutes=self.expires_in)

    def encode(self) -> TokenEncode:
        self.data.iat = self.iat
        self.data.exp = self.exp

        access_token = create_token(self.data, JWTConfig().access_token_secret_key)
        return TokenEncode(
            access_token=access_token,
            expires_in=self.expires_in,
            scope=self.scope,
            data=self.data,
        )

    @classmethod
    def decode(cls, token: str, scope: list[Role] | None = None) -> TokenDecode:
        decoded_dict = decode_token(token, JWTConfig().access_token_secret_key)

        if not decoded_dict:
            raise unprocessable_entity("Token invalid")

        decoded = TokenDecode.model_validate(decoded_dict)

        if scope:
            if Role.ADMIN in decoded.scope:
                ...
            elif not all(i in decoded.scope for i in scope):
                raise forbidden(msg="Insufficient scope.")

        return decoded
