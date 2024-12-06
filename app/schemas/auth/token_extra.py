import uuid
from datetime import UTC, datetime
from enum import Enum
from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict, EmailStr, computed_field

from app.schemas.auth.user import Role


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class AccessTokenData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    contract: Optional[str] = None


class RefreshTokenData(BaseModel):
    client_id: int
    scope: list[Role] = [Role.USER]

    @computed_field
    def uuid(self) -> UUID4:
        return uuid.uuid4()


class TokenEncode(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    data: AccessTokenData
    scope: list[Role] = [Role.USER]


class TokenDecode(BaseModel):
    iat: datetime
    exp: datetime
    scope: list[Role]
    data: AccessTokenData

    @computed_field()
    def expires_in(self) -> float:
        return (self.exp - datetime.now(UTC)).total_seconds()
