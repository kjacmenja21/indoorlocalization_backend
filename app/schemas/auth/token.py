from datetime import UTC, datetime, timedelta

from pydantic import BaseModel, Field, computed_field

from app.functions.exceptions import forbidden, unprocessable_entity
from app.functions.jwt import create_access_token, decode_access_token
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
        token = create_access_token(self)
        return TokenEncode(
            access_token=token,
            expires_in=self.expires_in,
            scope=self.scope,
            data=self.data,
        )

    @classmethod
    def decode(cls, token: str, scope: list[Role] | None = None) -> TokenDecode:
        decoded_dict = decode_access_token(token)

        if not decoded_dict:
            raise unprocessable_entity("Token invalid")

        decoded = Token.model_validate(decoded_dict)

        if scope:
            if "admin" in decoded.scope:
                ...
            elif not all(i in decoded.scope for i in scope):
                raise forbidden(msg="Insufficient scope.")

        return TokenDecode(**decoded.model_dump())
