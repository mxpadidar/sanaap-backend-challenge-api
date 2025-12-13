from datetime import timedelta

import pytest
from django.contrib.auth.models import User

from sanaap.exceptions import AuthFailedExc
from sanaap.handlers.login_handler import handle_user_login
from sanaap.services.jwt_service import JWTService

pytestmark = pytest.mark.django_db


@pytest.fixture
def creds() -> dict:
    return {"username": "login-user", "password": "secret!"}


@pytest.fixture
def token_ttl() -> timedelta:
    return timedelta(seconds=60)


@pytest.fixture
def user(creds: dict) -> User:
    return User.objects.create_user(**creds)


@pytest.mark.usefixtures("user")
def test_handle_user_login_returns_token_on_valid_credentials(
    jwt_service: JWTService, creds: dict, token_ttl: timedelta
):
    token = handle_user_login(jwt_service=jwt_service, token_ttl=token_ttl, **creds)
    assert isinstance(token, str)


@pytest.mark.usefixtures("user")
def test_handle_user_login_raises_unauth_for_unknown_username(
    jwt_service: JWTService, token_ttl: timedelta
):
    with pytest.raises(AuthFailedExc):
        handle_user_login(
            jwt_service=jwt_service,
            username="unknown-user",
            password="secret!",
            token_ttl=token_ttl,
        )


def test_handle_user_login_raises_unauth_for_wrong_password(
    jwt_service: JWTService, user: User, token_ttl: timedelta
):
    with pytest.raises(AuthFailedExc):
        handle_user_login(
            jwt_service=jwt_service,
            username=user.username,
            password="wrong-password",
            token_ttl=token_ttl,
        )
