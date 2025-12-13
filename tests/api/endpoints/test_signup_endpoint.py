import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def url() -> str:
    return reverse("signup")


def test_signup_endpoint_returns_201_and_creates_user(api_client: APIClient, url: str):
    payload = {"username": "test-user", "password": "secret"}
    response = api_client.post(url, data=payload)
    assert response.status_code == 201
    user = User.objects.get(username=payload["username"])
    assert user.check_password(payload["password"])


def test_signup_endpoint_accepts_optional_fields(api_client: APIClient, url: str):
    response = api_client.post(
        url,
        data={
            "username": "test-user",
            "password": "secret",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
        },
    )

    assert response.status_code == 201
    user = User.objects.get(username="test-user")
    assert user.email == "test@example.com"
    assert user.first_name == "Test"
    assert user.last_name == "User"


@pytest.mark.parametrize(
    "payload",
    [{"password": "secret"}, {"username": "login-user"}],
)
def test_signup_endpoint_returns_400_for_invalid_request_body(
    api_client: APIClient, url: str, payload
):
    response = api_client.post(url, data=payload)
    assert response.status_code == 400


def test_signup_endpoint_returns_409_when_email_is_duplicated(
    api_client: APIClient, url: str
):
    data = {"username": "un", "password": "secret!", "email": "test@example.com"}
    User.objects.create_user(**data)
    response = api_client.post(url, data=data)
    assert response.status_code == 409
