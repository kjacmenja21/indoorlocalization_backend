from datetime import UTC, datetime
from uuid import UUID

from pydantic import BaseModel, computed_field

from app.schemas.auth.user import Role


class TokenDecode(BaseModel):
    id: UUID
    iat: datetime
    exp: datetime
    scope: list[Role]

    @computed_field()
    def expires_in(self) -> float:
        return (self.exp - datetime.now(UTC)).total_seconds()
