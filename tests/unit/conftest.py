from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import MiddlewareItem, create_server
from app.models.common import Base


def mock_lifespan(_: FastAPI) -> Generator[None, Any, None]:
    yield


@pytest.fixture(scope="session", autouse=True)
def client() -> TestClient:
    """Creates a mocked FastAPI app for testing

    Returns:
        TestClient: This class will be used in each test involving API testing
    """
    middlewares = [
        MiddlewareItem(
            middleware_class=CORSMiddleware,
            config={
                "allow_origins": ["*"],
                "allow_credentials": True,
                "allow_methods": ["*"],
                "allow_headers": ["*"],
            },
        )
    ]
    app = create_server(mock_lifespan, middlewares)
    print("Created TestClient")
    return TestClient(app)


@pytest.fixture(scope="session")
def mock_session():
    """Fixture for mocking the database with SQLite and ORM"""
    # Setup SQLite in-memory database
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionMaker = sessionmaker(bind=engine)
    session = SessionMaker()

    yield session

    # Teardown mock database connection
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()
