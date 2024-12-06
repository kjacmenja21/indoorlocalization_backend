from datetime import UTC, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, computed_field

from app.schemas.auth.user import Role


class TokenData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    username: str
    iat: Optional[datetime] = None
    exp: Optional[datetime] = None
    scope: list[Role] = [Role.USER]


class TokenEncode(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    data: TokenData


class TokenDecode(TokenData):
    @computed_field()
    def expires_in(self) -> float:
        return (self.exp - datetime.now(UTC)).total_seconds()
