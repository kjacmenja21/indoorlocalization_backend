from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import MiddlewareItem, create_server
from app.models.common import Base
from app.models.user import UserRole
from app.schemas.auth.role_types import Role
from tests.unit.util import get_floormap


def create_user_roles(session: Session):
    # Define the function to create user roles
    admin_role = UserRole(name=Role.ADMIN)
    user_role = UserRole(name=Role.USER)
    session.add_all([admin_role, user_role])
    session.commit()


def create_users(session: Session):
    from app.models.user import User
    from app.schemas.api.user import UserCreate

    users_data = [
        UserCreate(
            username="admin",
            email="admin@example.com",
            plain_password="adminpass",
            role=Role.ADMIN,
        ),
        UserCreate(
            username="user",
            email="user@example.com",
            plain_password="userpass",
            role=Role.USER,
        ),
        UserCreate(
            username="testuser",
            email="testuser@example.com",
            plain_password="testpass",
            role=Role.USER,
        ),
        UserCreate(
            username="delete_user",
            email="delete_user@example.com",
            plain_password="deletepass",
            role=Role.USER,
        ),
    ]

    roles = session.query(UserRole).all()
    commit_users = []
    for user in users_data:
        commit_user = User(
            **user.model_dump(exclude_none=True, exclude=["plain_password", "role"])
        )
        commit_user.role = next(role for role in roles if role.name == user.role)
        commit_users.append(commit_user)

    session.add_all(commit_users)
    session.commit()


def create_floormaps(session: Session):
    floormaps = [
        get_floormap("First Floor 1"),
        get_floormap("Second Floor 1"),
        get_floormap("Third Floor 1"),
    ]
    session.add_all(floormaps)
    session.commit()


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
    Session = sessionmaker(bind=engine)
    session = Session()

    create_user_roles(session)
    create_users(session)
    create_floormaps(session)

    yield session

    # Teardown mock database connection
    session.close()
    Base.metadata.drop_all(engine)
