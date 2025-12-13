import pytest
from django.contrib.auth.models import User

from sanaap.exceptions import ConflictExc
from sanaap.handlers.signup_handler import handle_user_signup

pytestmark = pytest.mark.django_db


@pytest.fixture
def user_data() -> dict:
    return {"username": "login-user", "password": "secret!", "email": "login@mail.com"}


@pytest.fixture
def user(user_data: dict) -> User:
    return User.objects.create_user(**user_data)


def test_handle_user_signup_creates_new_user_with_valid_data(user_data: dict):
    user = handle_user_signup(**user_data)
    assert user.username == user_data["username"]
    assert User.objects.count() == 1


def test_handle_user_signup_raises_conflict_when_username_is_already_taken(user: User):
    with pytest.raises(ConflictExc):
        handle_user_signup(username=user.username, password="secret!")


def test_handle_user_signup_raises_conflict_when_email_is_already_taken(user: User):
    with pytest.raises(ConflictExc):
        handle_user_signup(username="user2", password="secret!", email=user.email)


def test_handle_user_signup_succeeds_when_email_is_not_provided(user_data: dict):
    user_data.pop("email", None)
    user = handle_user_signup(**user_data)
    assert user.email == ""
    assert User.objects.filter(username=user_data["username"]).exists()
