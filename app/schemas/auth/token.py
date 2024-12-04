from pydantic import BaseModel

from app.functions.exceptions import forbidden
from app.functions.jwt import decode_access_token
from app.schemas.auth.token_extra import TokenDecode
from app.schemas.auth.user import Role


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"

    @classmethod
    def decode(cls, token: str, scope: list[Role] | None = None) -> TokenDecode:
        decoded = decode_access_token(token)
        if scope:
            if "admin" in decoded["scope"]:
                ...
            elif not all(i in decoded["scope"] for i in scope):
                raise forbidden(msg="Insufficient scope.")
        return TokenDecode.model_validate(decoded)
