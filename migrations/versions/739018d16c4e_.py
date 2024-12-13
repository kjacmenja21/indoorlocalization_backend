"""empty message

Revision ID: 739018d16c4e
Revises: 97e23857f048
Create Date: 2024-12-12 14:17:54.660430

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "739018d16c4e"
down_revision: Union[str, None] = "97e23857f048"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        table_name="users", column_name="contract", new_column_name="contact"
    )


def downgrade() -> None:
    op.alter_column(
        table_name="users", column_name="contact", new_column_name="contract"
    )
