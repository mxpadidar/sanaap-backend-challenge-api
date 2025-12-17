import pytest
from django.conf import settings
from django.contrib.auth.models import Group, User
from rest_framework.test import APIClient

from sanaap.services import JWTService


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="session")
def jwt_service() -> JWTService:
    return JWTService(secret_key=settings.JWT_SECRET)


@pytest.fixture
def creds() -> dict:
    return {
        "normal": {"username": "normal", "password": "normal"},
        "staff": {"username": "staff", "password": "staff"},
        "admin": {"username": "admin", "password": "admin"},
    }


@pytest.fixture
def normal_group() -> Group:
    return Group.objects.create(name="normal")


@pytest.fixture
def normal_user(creds: dict, normal_group: Group) -> User:
    normal = User.objects.create_user(**creds["normal"])
    normal.groups.add(normal_group)
    return normal
