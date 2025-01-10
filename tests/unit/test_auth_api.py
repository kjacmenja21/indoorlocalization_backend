import pytest

from app.schemas.api.user import UserModelIndentified


# Mock the dependencies
@pytest.fixture
def mock_user_service():
    class MockUserService:
        def authenticate_user(self, username, password):
            if username == "valid_user" and password == "valid_pass":
                return UserModelIndentified(id=1, username="valid_user", role="user")
            return None

        def get_user(self, user):
            if user == 1:
                return UserModelIndentified(id=1, username="valid_user", role="user")
            return None

    return MockUserService()


@pytest.fixture
def mock_check_refresh_token_cookie():
    def mock_refresh_token_cookie():
        return "valid_refresh_token"

    return mock_refresh_token_cookie


@pytest.fixture
def mock_general_config():
    class MockGeneralConfig:
        jwt_refresh_token_secret_key = "secret_key"
        jwt_access_token_expire_minutes = 15
        refresh_token_cookie_name = "refresh_token"

    return MockGeneralConfig()


def create_url(url: str):
    return "/api/v1/" + url


def test_login_valid(client, mock_user_service):
    # Mock form data
    url = create_url("auth/login")
    form_data = {"username": "valid_user", "password": "valid_pass"}
    response = client.post(url, data=form_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.cookies


def test_login_invalid(client, mock_user_service):
    # Mock form data
    url = create_url("auth/login")
    form_data = {"username": "invalid_user", "password": "wrong_pass"}
    response = client.post(url, data=form_data)
    assert response.status_code == 401  # Unauthorized


def test_autologin_valid(
    client, mock_user_service, mock_check_refresh_token_cookie, mock_general_config
):
    # Mock valid refresh token
    url = create_url("auth/autologin")
    refresh_token = "valid_refresh_token"
    response = client.post(url, cookies={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.cookies


def test_autologin_invalid_token(
    client, mock_user_service, mock_check_refresh_token_cookie
):
    # Test invalid refresh token
    url = create_url("auth/autologin")
    refresh_token = "invalid_refresh_token"
    response = client.post(url, cookies={"refresh_token": refresh_token})
    assert response.status_code == 401  # Unauthorized
