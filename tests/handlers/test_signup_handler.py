import pytest
from django.contrib.auth.models import Group, User

from sanaap.exceptions import ConflictExc
from sanaap.handlers.signup_handler import handle_user_signup

pytestmark = pytest.mark.django_db


@pytest.fixture
def user_data() -> dict:
    return {
        "default_group": "normal",
        "username": "new-user",
        "password": "secret!",
        "email": "login@mail.com",
    }


def test_handle_user_signup_creates_new_user_with_valid_data(
    user_data: dict, normal_group: Group
):
    user = handle_user_signup(**user_data)
    assert user.username == user_data["username"]
    assert User.objects.filter(username=user_data["username"]).exists()
    assert normal_group in user.groups.all()


def test_handle_user_signup_raises_conflict_on_existing_username(normal_user: User):
    with pytest.raises(ConflictExc):
        handle_user_signup(
            default_group="normal", username=normal_user.username, password="secret!"
        )


def test_handle_user_signup_raises_conflict_on_existing_email(normal_user: User):
    with pytest.raises(ConflictExc):
        handle_user_signup(
            default_group="normal",
            username="normal2",
            password="secret!",
            email=normal_user.email,
        )


@pytest.mark.usefixtures("normal_group")
def test_handle_user_signup_succeeds_when_email_is_not_provided(user_data: dict):
    user_data.pop("email", None)
    user = handle_user_signup(**user_data)
    assert user.email == ""
    assert User.objects.filter(username=user_data["username"]).exists()
