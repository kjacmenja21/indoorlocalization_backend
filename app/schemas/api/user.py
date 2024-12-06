from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, computed_field, field_validator

from app.functions.jwt import generate_salt, get_password_hash
from app.schemas.auth.user import Role


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    plain_password: str
    role: Role = Role.USER

    @computed_field
    @property
    def salt(self) -> bytes:
        return generate_salt()

    @computed_field
    @property
    def password(self) -> bytes:
        return get_password_hash(self.plain_password, self.salt)[0]

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
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    contract: Optional[str] = None
    password: bytes
    salt: bytes
    role: Optional[UserRoleModel] = None
