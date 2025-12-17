import datetime

import pytest
from django.contrib.auth.models import User
from rest_framework import exceptions
from rest_framework.test import APIRequestFactory

from sanaap.api.auth import TokenAuth
from sanaap.services import JWTService

pytestmark = pytest.mark.django_db


@pytest.fixture
def jwt_auth() -> TokenAuth:
    return TokenAuth()


@pytest.fixture
def reqmaker() -> APIRequestFactory:
    return APIRequestFactory()


def test_authenticate_returns_user_and_token(
    reqmaker: APIRequestFactory,
    jwt_auth: TokenAuth,
    jwt_service: JWTService,
    normal_user: User,
):
    token = jwt_service.encode(
        sub=normal_user.username, ttl=datetime.timedelta(minutes=5)
    )

    request = reqmaker.get("/", HTTP_AUTHORIZATION=f"Bearer {token}")
    authuser, authtoken = jwt_auth.authenticate(request)
    assert isinstance(authuser, User)
    assert authuser.username == normal_user.username
    assert authtoken == token


def test_authenticate_fails_when_authorization_header_missing(
    reqmaker: APIRequestFactory, jwt_auth: TokenAuth
):
    request = reqmaker.get("/")
    with pytest.raises(exceptions.AuthenticationFailed):
        jwt_auth.authenticate(request)


def test_authenticate_fails_on_invalid_header_format(
    reqmaker: APIRequestFactory, jwt_auth: TokenAuth
):
    request = reqmaker.get("/", HTTP_AUTHORIZATION="InvalidHeader")
    with pytest.raises(exceptions.AuthenticationFailed):
        jwt_auth.authenticate(request)


def test_authenticate_fails_on_invalid_token(
    reqmaker: APIRequestFactory, jwt_auth: TokenAuth
):
    request = reqmaker.get("/", HTTP_AUTHORIZATION="Bearer invalid.token.value")
    with pytest.raises(exceptions.AuthenticationFailed):
        jwt_auth.authenticate(request)
