import logging
import typing

from django.contrib.auth.models import User

from sanaap.exceptions import ConflictExc

logger = logging.getLogger(__name__)


class SignupData(typing.TypedDict):
    username: str
    password: str
    email: typing.NotRequired[str]
    first_name: typing.NotRequired[str]
    last_name: typing.NotRequired[str]


def handle_user_signup(**data: typing.Unpack[SignupData]) -> User:
    """Create a new user while enforcing unique username and email constraints."""

    if User.objects.filter(username=data["username"]).exists():
        logger.debug(f"duplicated {data['username']=}")
        raise ConflictExc("Username already taken.")

    if "email" in data and User.objects.filter(email=data["email"]).exists():
        logger.debug(f"duplicated {data['email']=}")
        raise ConflictExc("Email already taken.")

    return User.objects.create_user(**data)
