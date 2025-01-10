from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, sessionmaker

from app import create_server
from app.models.common import Base


@pytest.fixture(scope="module")
def mock_engine() -> Generator[Engine, Any, None]:
    """Create an in-memory SQLite database for testing"""
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def mock_session(mock_engine) -> Generator[Session, Any, None]:
    """Create a session to interact with the mock in-memory database"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=mock_engine)
    db = SessionLocal()
    yield db
    db.close()


def mock_lifespan(_: FastAPI) -> Generator[None, Any, None]:

    yield


@pytest.fixture(scope="session", autouse=True)
def client() -> TestClient:
    """Creates a mocked FastAPI app for testing

    Returns:
        TestClient: This class will be used in each test involving API testing
    """
    app = create_server(mock_lifespan, [])
    print("Created TestClient")
    return TestClient(app)
