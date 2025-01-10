from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app import create_server


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
