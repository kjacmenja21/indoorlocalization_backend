from datetime import UTC, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, computed_field

from app.schemas.auth.user import Role


class TokenData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    contract: Optional[str] = None


class TokenEncode(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    data: TokenData
    scope: list[Role] = [Role.USER]


class TokenDecode(BaseModel):
    id: UUID
    iat: datetime
    exp: datetime
    scope: list[Role]
    data: TokenData

    @computed_field()
    def expires_in(self) -> float:
        return (self.exp - datetime.now(UTC)).total_seconds()
