from typing import Any

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import CursorResult, Engine, inspect

from app import config


def is_database_up_to_date(input_engine: Engine, alembic_cfg: Config) -> bool:
    """
    Check if the database has already been initialized by looking
    for the `alembic_version` table.
    """
    inspector = inspect(input_engine)

    if not inspector.has_table("alembic_version"):
        return False

    with input_engine.begin() as connection:
        cursor: CursorResult[Any] = connection.execute(
            "SELECT version_num FROM alembic_version"
        )
        result = cursor.fetchone()
        if not result:
            return False  # No version number found

        current_version = result[0]

    script = ScriptDirectory.from_config(alembic_cfg)
    head_version = script.get_current_head()

    return current_version == head_version


def upgrade_database(alembic_cfg: Config) -> None:
    command.upgrade(alembic_cfg, "head")


def prepare_database(engine: Engine, alembic_config: Config):
    if is_database_up_to_date(engine, config):
        upgrade_database(alembic_config)