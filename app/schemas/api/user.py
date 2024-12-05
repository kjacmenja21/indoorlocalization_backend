from typing import Optional

from pydantic import BaseModel, EmailStr

from app.schemas.auth.user import Role


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    roleId: Role = Role.USER


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
