import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def url() -> str:
    return reverse("login")


@pytest.fixture
def creds() -> dict:
    return {"username": "login-user", "password": "secret!"}


@pytest.fixture
def user(creds: dict) -> User:
    return User.objects.create_user(**creds)


@pytest.mark.usefixtures("user")
def test_login_endpoint_returns_200_on_valid_credentials(
    api_client: APIClient, url: str, creds: dict
):
    response = api_client.post(url, data=creds)

    assert response.status_code == 200
    assert "access_token" in response.data
    assert response.data.get("access_token")


@pytest.mark.usefixtures("user")
def test_login_endpoint_returns_401_on_wrong_password(
    api_client: APIClient, url: str, creds: dict
):
    response = api_client.post(
        url, data={"username": creds["username"], "password": "wrong-password"}
    )
    assert response.status_code == 401


@pytest.mark.usefixtures("user")
def test_login_endpoint_returns_401_on_unknown_user(api_client: APIClient, url: str):
    response = api_client.post(
        url, data={"username": "unknown-user", "password": "any-secret"}
    )
    assert response.status_code == 401


@pytest.mark.parametrize(
    "payload",
    [{"password": "secret"}, {"username": "login-user"}],
)
def test_login_endpoint_returns_400_for_invalid_request_body(
    api_client: APIClient, url: str, payload
):
    response = api_client.post(url, data=payload)
    assert response.status_code == 400
