import pytest
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from sanaap import services


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="session")
def jwt_service() -> services.JWTService:
    return services.JWTService(secret_key=settings.JWT_SECRET)


@pytest.fixture
def normal_user() -> User:
    return User.objects.create(username="normal", password="secret!")
