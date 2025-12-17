from datetime import timedelta

import pytest
from django.contrib.auth.models import User

from sanaap.exceptions import AuthFailedExc
from sanaap.handlers.login_handler import handle_user_login
from sanaap.services.jwt_service import JWTService

pytestmark = pytest.mark.django_db


@pytest.fixture
def token_ttl() -> timedelta:
    return timedelta(seconds=60)


@pytest.mark.usefixtures("normal_user")
def test_handle_user_login_returns_token_on_valid_credentials(
    jwt_service: JWTService, creds: dict, token_ttl: timedelta
):
    token = handle_user_login(
        jwt_service=jwt_service, token_ttl=token_ttl, **creds["normal"]
    )
    assert isinstance(token, str)
    assert token  # non-empty token


@pytest.mark.usefixtures("normal_user")
def test_handle_user_login_raises_unauth_for_nonexist_username(
    jwt_service: JWTService, token_ttl: timedelta
):
    with pytest.raises(AuthFailedExc):
        handle_user_login(
            jwt_service=jwt_service,
            username="nonexist",
            password="secret!",
            token_ttl=token_ttl,
        )


def test_handle_user_login_raises_unauth_for_wrong_password(
    jwt_service: JWTService, normal_user: User, token_ttl: timedelta
):
    with pytest.raises(AuthFailedExc):
        handle_user_login(
            jwt_service=jwt_service,
            username=normal_user.username,
            password="wrong-password",
            token_ttl=token_ttl,
        )
