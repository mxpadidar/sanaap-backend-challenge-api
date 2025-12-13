import pytest

from sanaap.container import container
from sanaap.services import JWTService


def test_container_can_resolve_registered_service():
    service = container.resolve(JWTService)
    assert isinstance(service, JWTService)


def test_container_returns_same_instance_for_repeated_resolution():
    first = container.resolve(JWTService)
    second = container.resolve(JWTService)

    assert first is second


def test_container_fails_when_service_is_not_registered():
    class UnknownService:
        pass

    with pytest.raises(Exception):
        container.resolve(UnknownService)
