import pytest
from django.conf import settings
from rest_framework.test import APIClient

from sanaap import services


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="session")
def jwt_service() -> services.JWTService:
    return services.JWTService(secret_key=settings.JWT_SECRET)
