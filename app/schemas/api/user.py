from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    SecretStr,
    computed_field,
    field_validator,
)

from app.functions.jwt import generate_salt, get_password_hash
from app.schemas.auth.user import Role


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    contract: Optional[str] = None


class UserCreate(UserBase):
    plain_password: SecretStr
    role: Role = Role.USER

    @computed_field
    @property
    def salt(self) -> bytes:
        return generate_salt()

    @computed_field
    @property
    def password(self) -> bytes:
        return get_password_hash(self.plain_password, self.salt)[0]

    @classmethod
    @field_validator("role", mode="before")
    def validate_lowercase(cls, value):
        if not isinstance(value, str):
            raise ValueError("role must be a string")
        return value.lower()


class UserRoleModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: Role


class UserModel(UserBase):
    model_config = ConfigDict(from_attributes=True)
    role: Optional[UserRoleModel] = None


class UserModelIndentified(UserModel):
    id: int


class UserModelCredentials(UserModel):
    password: bytes
    salt: bytes
