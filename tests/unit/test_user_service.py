from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.database.services.user_service import UserService
from app.models.user import User, UserRole
from app.schemas.api.user import UserBase, UserCreate, UserModelIndentified
from app.schemas.auth.role_types import Role
from tests.unit.util import create_user_roles, create_users


@pytest.fixture
def user_service(mock_session: Session) -> UserService:
    return UserService(session=mock_session)


@pytest.fixture(autouse=True)
def cleanup_zones(mock_session: Session):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    create_user_roles(mock_session)
    create_users(mock_session)
    yield  # this is where the testing happens

    # Teardown : fill with any logic you want
    mock_session.query(User).delete()
    mock_session.query(UserRole).delete()


def test_authenticate_user(user_service: UserService, mock_session: Session):
    result = user_service.authenticate_user("testuser", "testpass")
    expected = {
        "username_is_testuser": True,
    }

    actual = {
        "username_is_testuser": result.username == "testuser",
    }

    assert expected == actual


def test_create_user(user_service: UserService, mock_session: Session):
    user_create = UserCreate(
        username="newuser",
        email="newuser@example.com",
        plain_password="password",
        role=Role.USER,
    )

    result = user_service.create_user(user_create)

    expected = {
        "username_is_newuser": True,
        "role_is_user": True,
    }

    actual = {
        "username_is_newuser": result.username == "newuser",
        "role_is_user": result.role.name == "user",
    }

    assert expected == actual


def test_delete_user(user_service: UserService, mock_session: Session):

    user = mock_session.query(User).where(User.username == "delete_user").first()
    user_id = user.id
    result = user_service.delete_user(user_id)

    expected = {"user_is_deleted": True, "user_id_doesnt_exist": None}
    actual = {
        "user_is_deleted": result,
        "user_id_doesnt_exist": mock_session.query(User)
        .where(User.id == user_id)
        .first(),
    }

    assert expected == actual


def test_get_all_users(user_service: UserService, mock_session: Session):
    user_count = mock_session.query(User).count()

    result = user_service.get_all_users()
    expected = {
        "users_count_greater_than_zero": True,
        "all_users_in_result": True,
    }

    actual = {
        "users_count_greater_than_zero": len(result) > 0,
        "all_users_in_result": len(result) == user_count,
    }

    assert expected == actual


def test_get_user(user_service: UserService, mock_session: Session):
    user = mock_session.query(User).where(User.username == "testuser").first()

    result = user_service.get_user(user.id)

    assert result.username == "testuser"


def test_user_exists(user_service: UserService, mock_session: Session):
    users = mock_session.query(User).all()
    user_ids = [user.id for user in users]

    results = []
    for user_id in user_ids:
        results.append(user_service.user_exists(user_id))

    assert all(results)


def test_user_from_orm(user_service: UserService, mock_session: Session):
    user = mock_session.query(User).where(User.username == "testuser").first()

    result = user_service.user_from_orm(user)

    expected = {
        "username_is_testuser": True,
        "role_is_correct": True,
    }

    actual = {
        "username_is_testuser": result.username == "testuser",
        "role_is_correct": result.role.name == user.role.name,
    }

    assert expected == actual
