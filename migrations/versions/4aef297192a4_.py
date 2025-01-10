"""empty message

Revision ID: 4aef297192a4
Revises: 21dc04570d2d
Create Date: 2025-01-10 19:04:04.161595

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4aef297192a4"
down_revision: Union[str, None] = "21dc04570d2d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "floorMap",
        sa.Column(
            "image_type", sa.String(length=10), nullable=False, server_default="png"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("floorMap", "image_type")
    # ### end Alembic commands ###