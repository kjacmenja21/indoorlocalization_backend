"""empty message

Revision ID: 97e23857f048
Revises: 5f28db645842
Create Date: 2024-12-11 22:31:45.871981

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from app.config import FastAPISettings
from app.functions.jwt_functions import get_password_hash
from app.schemas.auth.role_types import Role

# revision identifiers, used by Alembic.
revision: str = "97e23857f048"
down_revision: Union[str, None] = "5f28db645842"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    config = FastAPISettings()
    password, salt = get_password_hash(config.password, None)
    user_role_table = sa.table("userRole", sa.column("name", sa.String))

    connection = op.get_bind()

    # Fetch roleId for the admin role
    role_id_result = connection.execute(
        sa.text('SELECT id FROM "userRole" WHERE name = :role_name'),
        {"role_name": Role.ADMIN.value.lower()},  # Assuming Role.ADMIN is Enum
    ).scalar()

    connection.execute(
        sa.text(
            """
            INSERT INTO users (username, email, first_name, last_name, contract, password, salt, "roleId")
            VALUES (:username, :email, :first_name, :last_name, :contract, :password, :salt, :role_id)
            """
        ),
        {
            "username": config.admin,
            "email": "example@email.com",
            "first_name": "first_name",
            "last_name": "last_name",
            "contract": "-",
            "password": password,  # Convert bytes to hex string
            "salt": salt,  # Convert bytes to hex string
            "role_id": role_id_result,
        },
    )


def downgrade() -> None:
    config = FastAPISettings()

    op.execute(
        f"""
               DELETE FROM users WHERE username = '{config.admin}' 
               and roleId = (SELECT id FROM userRole WHERE name = '{Role.ADMIN}')
               """
    )
