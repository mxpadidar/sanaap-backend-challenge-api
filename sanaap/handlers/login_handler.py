import logging
import typing
from datetime import timedelta

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

from sanaap.exceptions import AuthFailedExc
from sanaap.services import JWTService

logger = logging.getLogger(__name__)


class LoginData(typing.TypedDict):
    username: str
    password: str
    token_ttl: timedelta


def handle_user_login(jwt_service: JWTService, **data: typing.Unpack[LoginData]) -> str:
    user = User.objects.filter(username=data["username"], is_active=True).first()
    if user is None or not check_password(data["password"], user.password):
        raise AuthFailedExc("Authentication Failed")
    return jwt_service.encode(sub=user.username, ttl=data["token_ttl"])
