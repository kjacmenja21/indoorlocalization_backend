from typing import Generator

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.database.db import DBEngineHandler
from app.database.settings import db_settings as settings


@pytest.fixture
def db_engine_handler() -> DBEngineHandler:
    return DBEngineHandler(
        url="sqlite:///:memory:",
    )


def test_db_engine_handler_init(db_engine_handler: DBEngineHandler):
    assert isinstance(db_engine_handler, DBEngineHandler)
    assert isinstance(db_engine_handler.engine, Engine)


def test_get_engine(db_engine_handler: DBEngineHandler):
    engine = db_engine_handler.get_engine()
    assert isinstance(engine, Engine)


def test_get_sessionmaker(db_engine_handler: DBEngineHandler):
    session_maker = db_engine_handler.get_sessionmaker()
    assert callable(session_maker)
    assert isinstance(session_maker(), Session)


def test_get_db_session(db_engine_handler: DBEngineHandler):
    assert isinstance(db_engine_handler.get_db_session(), Generator)


def test_get_db_session_ctx(db_engine_handler: DBEngineHandler):
    with db_engine_handler.get_db_session_ctx() as session:
        assert isinstance(session, Session)
