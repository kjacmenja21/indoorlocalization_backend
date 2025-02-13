"""empty message

Revision ID: 21dc04570d2d
Revises: 9d5e86499055
Create Date: 2024-12-29 16:20:20.468449

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "21dc04570d2d"
down_revision: Union[str, None] = "9d5e86499055"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "assetZoneHistory",
        "exitDateTime",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "assetZoneHistory",
        "exitDateTime",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
    )
    # ### end Alembic commands ###
