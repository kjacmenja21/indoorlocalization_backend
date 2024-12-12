from datetime import UTC, datetime, timedelta
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, computed_field

from app.config import GeneralConfig
from app.schemas.api.user import UserRoleModel
from app.schemas.auth.user import Role


class RefreshTokenData(BaseModel):
    client_id: int
    iat: datetime = Field(default_factory=lambda: datetime.now(UTC))
    expires_in: int = GeneralConfig().jwt_refresh_token_expire_minutes

    @computed_field
    def exp(self) -> datetime:
        return self.iat + timedelta(minutes=self.expires_in)


class TokenData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    first_name: str
    first_name: str
    contact: str
    role: UserRoleModel
    iat: Optional[datetime] = None
    exp: Optional[datetime] = None
    scope: list[Role] = [Role.USER]


class TokenEncode(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    data: TokenData


class TokenDecode(TokenData):
    @computed_field()
    def expires_in(self) -> float:
        return (self.exp - datetime.now(UTC)).total_seconds()
