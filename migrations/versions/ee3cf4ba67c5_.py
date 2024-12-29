"""update zonePoint schema

Revision ID: ee3cf4ba67c5
Revises: 8d795357a292
Create Date: 2024-12-28 20:17:45.200535
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ee3cf4ba67c5"
down_revision: Union[str, None] = "8d795357a292"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Drop existing primary key constraint on zonePoint table
    op.drop_constraint("zonePoint_pkey", "zonePoint", type_="primary")

    # Remove default value for zoneId
    op.alter_column("zonePoint", "zoneId", server_default=None)

    # Add updated primary key constraint with both zoneId and ordinalNumber
    op.create_primary_key("zonePoint_pkey", "zonePoint", ["zoneId", "ordinalNumber"])

    # Ensure zoneId references zone.id
    op.create_foreign_key("fk_zonePoint_zone", "zonePoint", "zone", ["zoneId"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Drop the updated primary key constraint
    op.drop_constraint("zonePoint_pkey", "zonePoint", type_="primary")

    # Restore default value for zoneId
    op.alter_column(
        "zonePoint",
        "zoneId",
        server_default=sa.text("""nextval('"zonePoint_zoneId_seq"'::regclass)"""),
    )

    # Revert to the original primary key on zoneId only
    op.create_primary_key("zonePoint_pkey", "zonePoint", ["zoneId"])

    # Drop foreign key constraint
    op.drop_constraint("fk_zonePoint_zone", "zonePoint", type_="foreignkey")
    # ### end Alembic commands ###