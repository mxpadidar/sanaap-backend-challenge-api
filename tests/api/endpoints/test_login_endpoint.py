import pytest
from django.urls import reverse
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def url() -> str:
    return reverse("login")


@pytest.mark.usefixtures("normal_user")
def test_login_endpoint_returns_200_on_valid_credentials(
    api_client: APIClient, url: str, creds: dict
):
    response = api_client.post(url, data=creds["normal"])
    assert response.status_code == 200
    assert "access_token" in response.data
    assert isinstance(response.data["access_token"], str)
    assert response.data["access_token"]


@pytest.mark.usefixtures("normal_user")
def test_login_endpoint_returns_401_on_wrong_password(
    api_client: APIClient, url: str, creds: dict
):
    response = api_client.post(
        url,
        data={
            "username": creds["normal"]["username"],
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401


@pytest.mark.usefixtures("normal_user")
def test_login_endpoint_returns_401_on_nonexist_username(api_client: APIClient, url: str):
    response = api_client.post(url, data={"username": "nonexist", "password": "secret!"})
    assert response.status_code == 401


@pytest.mark.parametrize(
    "payload", [{"password": "secret!"}, {"username": "login-user"}, {}]
)
def test_login_endpoint_returns_400_for_invalid_request_body(
    api_client: APIClient, url: str, payload: dict
):
    response = api_client.post(url, data=payload)
    assert response.status_code == 400
