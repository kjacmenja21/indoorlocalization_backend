from typing import Optional

from pydantic import BaseModel, EmailStr

from app.schemas.auth.user import Role


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    roleId: Role = Role.USER


class UserRoleModel(BaseModel):
    id: int
    name: str


class UserModel(BaseModel):
    email: str
    first_name: str
    last_name: str
    contract: str
    password: str
    salt: str
    roleId: Optional[UserRoleModel]
