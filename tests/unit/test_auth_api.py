import pytest


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


def test_login_valid(client):
    # Mock form data
    url = create_url("auth/login")
    form_data = {"username": "valid_user", "password": "valid_pass"}
    response = client.post(url, data=form_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.cookies


def test_login_invalid(client):
    # Mock form data
    url = create_url("auth/login")
    form_data = {"username": "invalid_user", "password": "wrong_pass"}
    response = client.post(url, data=form_data)
    assert response.status_code == 401  # Unauthorized
