"""empty message

Revision ID: eabaed5158f0
Revises: 739018d16c4e
Create Date: 2024-12-12 23:58:15.492694

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "eabaed5158f0"
down_revision: Union[str, None] = "739018d16c4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE "floorMap" 
        ALTER COLUMN image TYPE BYTEA 
        USING lo_get(image);
        """
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "floorMap",
        "image",
        existing_type=postgresql.BYTEA(),
        type_=postgresql.OID(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
