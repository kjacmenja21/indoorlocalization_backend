"""Add cascade delete behavior to ZonePoint

Revision ID: 9d5e86499055
Revises: ee3cf4ba67c5
Create Date: 2024-12-29 11:28:46.489047

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9d5e86499055"
down_revision: Union[str, None] = "ee3cf4ba67c5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the existing foreign key constraint (if exists) using raw SQL
    op.execute(
        """
        ALTER TABLE "zonePoint" DROP CONSTRAINT IF EXISTS "zonePoint_zoneId_fkey";
    """
    )

    # Recreate the foreign key with ON DELETE CASCADE
    op.create_foreign_key(
        "zonePoint_zoneId_fkey",  # New foreign key constraint name
        "zonePoint",  # Source table
        "zone",  # Referenced table
        ["zoneId"],  # Local column(s)
        ["id"],  # Referenced column(s)
        ondelete="CASCADE",  # Enforce cascading delete
    )


def downgrade() -> None:
    # Revert the foreign key constraint to its original form
    op.execute(
        """
        ALTER TABLE "zonePoint" DROP CONSTRAINT IF EXISTS "zonePoint_zoneId_fkey";
    """
    )

    op.create_foreign_key(
        "zonePoint_zoneId_fkey", "zonePoint", "zone", ["zoneId"], ["id"]
    )
