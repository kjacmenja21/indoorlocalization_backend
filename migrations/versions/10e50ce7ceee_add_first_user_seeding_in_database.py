"""Add first user seeding in database

Revision ID: 10e50ce7ceee
Revises: 65af5b6dcfe5
Create Date: 2024-12-11 21:47:16.203860

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from app.api.dependencies import get_user_service
from app.config import FastAPISettings
from app.schemas.api.user import UserCreate
from app.schemas.auth.user import Role

# revision identifiers, used by Alembic.
revision: str = "10e50ce7ceee"
down_revision: Union[str, None] = "65af5b6dcfe5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    config = FastAPISettings()
    user = UserCreate(
        username=config.admin, plain_password=config.password, role=Role.ADMIN
    )
    service = get_user_service()
    service.create_user(user)


def downgrade() -> None:
    pass
