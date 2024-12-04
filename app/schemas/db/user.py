from typing import Optional

from pydantic import BaseModel


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
