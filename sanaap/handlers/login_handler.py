import logging
import typing
from datetime import timedelta

from django.contrib.auth import authenticate

from sanaap.exceptions import AuthFailedExc
from sanaap.services import JWTService

logger = logging.getLogger(__name__)


class LoginData(typing.TypedDict):
    username: str
    password: str
    token_ttl: timedelta


def handle_user_login(jwt_service: JWTService, **data: typing.Unpack[LoginData]) -> str:
    user = authenticate(username=data["username"], password=data["password"])
    if user is None or not user.is_active:
        raise AuthFailedExc("Authentication Failed")
    return jwt_service.encode(sub=user.get_username(), ttl=data["token_ttl"])
