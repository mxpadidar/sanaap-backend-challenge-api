import functools
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import authentication, exceptions
from rest_framework.request import Request

from sanaap.container import container
from sanaap.services import JWTService

logger = logging.getLogger(__name__)


class TokenAuth(authentication.TokenAuthentication):
    keyword = "Bearer"

    @functools.cached_property
    def jwt(self) -> JWTService:
        return container.resolve(JWTService)  # type: ignore

    def authenticate(self, request: Request) -> tuple[User, str]:
        result = super().authenticate(request)
        if result is None:
            raise exceptions.AuthenticationFailed
        return result

    def authenticate_credentials(self, key: str) -> tuple[User, str]:
        try:
            username = self.jwt.decode(key)
        except ValueError:
            raise exceptions.AuthenticationFailed("Invalid or expired token.")
        user = (
            User.objects.prefetch_related(
                "groups", "groups__permissions", "user_permissions"
            )
            .filter(username=username, is_active=True)
            .first()
        )
        if user is None:
            raise exceptions.AuthenticationFailed("Authentication failed.")
        return user, key

    def get_user(self, username: str) -> User | None:
        cache_key = f"user:{username}"
        user = cache.get(cache_key)
        if user:
            return user
        user = (
            User.objects.prefetch_related(
                "groups", "groups__permissions", "user_permissions"
            )
            .filter(username=username, is_active=True)
            .first()
        )

        if user is not None:
            cache.set(cache_key, user, settings.AUTH_USER_CACHE_TTL_SEC)
        return user
