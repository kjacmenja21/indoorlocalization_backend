"""empty message

Revision ID: 5f28db645842
Revises: 65af5b6dcfe5
Create Date: 2024-12-11 22:15:11.199275

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from app.config import FastAPISettings
from app.functions.jwt import get_password_hash
from app.schemas.auth.user import Role

# revision identifiers, used by Alembic.
revision: str = "5f28db645842"
down_revision: Union[str, None] = "65af5b6dcfe5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_role_table = sa.table("userRole", sa.column("name", sa.String))

    for role in Role:
        op.execute(user_role_table.insert().values(name=role.value.lower()))


def downgrade() -> None:
    user_role_table = sa.table("userRole", sa.column("name", sa.String))

    for role in Role:
        op.execute(user_role_table.delete().where(name=role.value))
