"""empty message

Revision ID: 83d27a7c4977
Revises: eabaed5158f0
Create Date: 2024-12-13 15:59:06.686605

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "83d27a7c4977"
down_revision: Union[str, None] = "eabaed5158f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename 'lastSync' column to 'last_sync'
    op.alter_column(
        "asset",
        "lastSync",
        new_column_name="last_sync",
        existing_type=sa.TIMESTAMP(),
        nullable=False,
    )

    # Rename 'floorMapId' column to 'floormap_id'
    op.alter_column(
        "asset",
        "floorMapId",
        new_column_name="floormap_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )


def downgrade() -> None:
    # Rename 'last_sync' column back to 'lastSync'
    op.alter_column(
        "asset",
        "last_sync",
        new_column_name="lastSync",
        existing_type=sa.TIMESTAMP(),
        nullable=False,
    )

    # Rename 'floormap_id' column back to 'floorMapId'
    op.alter_column(
        "asset",
        "floormap_id",
        new_column_name="floorMapId",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
