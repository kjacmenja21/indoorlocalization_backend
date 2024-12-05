from typing import Optional

from pydantic import BaseModel, EmailStr, computed_field

from app.functions.jwt import generate_salt, get_password_hash
from app.schemas.auth.user import Role


class UserCreate(BaseModel):
    email: EmailStr
    plain_password: str
    roleId: Role = Role.USER

    @computed_field
    @property
    def salt(self) -> bytes:
        return generate_salt()

    @computed_field
    @property
    def password(self) -> bytes:
        return get_password_hash(self.plain_password, self.salt)


class UserRoleModel(BaseModel):
    id: int
    name: Role


class UserModel(BaseModel):
    email: EmailStr
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    contract: Optional[str]
    password: bytes
    salt: bytes
    roleId: Optional[UserRoleModel]
