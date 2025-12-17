import logging
import typing

from django.contrib.auth.models import Group, User

from sanaap.exceptions import ConflictExc, InternalErr

logger = logging.getLogger(__name__)


class SignupData(typing.TypedDict):
    username: str
    password: str
    email: typing.NotRequired[str]
    first_name: typing.NotRequired[str]
    last_name: typing.NotRequired[str]


def handle_user_signup(default_group: str, **data: typing.Unpack[SignupData]) -> User:
    if User.objects.filter(username=data["username"]).exists():
        logger.debug(f"duplicated {data['username']=}")
        raise ConflictExc("Username already taken.")

    if "email" in data and User.objects.filter(email=data["email"]).exists():
        logger.debug(f"duplicated {data['email']=}")
        raise ConflictExc("Email already taken.")

    try:
        group = Group.objects.get(name=default_group)
    except Group.DoesNotExist:
        logger.critical(f"{default_group=} does not exists")
        raise InternalErr("Signup service is unavailable.")

    user = User.objects.create_user(**data)
    user.groups.add(group)

    return user
