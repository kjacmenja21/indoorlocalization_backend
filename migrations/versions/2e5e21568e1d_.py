from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "2e5e21568e1d"
down_revision: Union[str, None] = "83d27a7c4977"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Alter the 'active' column to change its type from BIT to BOOLEAN
    op.alter_column(
        "asset",
        "active",
        existing_type=postgresql.BIT(length=1),
        type_=sa.Boolean(),
        existing_nullable=False,
        postgresql_using="(active::text = '1')::boolean",
    )  # Convert BIT to BOOLEAN


def downgrade() -> None:
    # Revert the 'active' column back from BOOLEAN to BIT
    op.alter_column(
        "asset",
        "active",
        existing_type=sa.Boolean(),
        type_=postgresql.BIT(length=1),
        existing_nullable=False,
        postgresql_using="(active::boolean)::bit",
    )  # Convert BOOLEAN to BIT
