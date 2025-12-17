import io
import uuid
from typing import Generator

import minio
import pytest
from django.conf import settings
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from sanaap.docs.models import Document
from sanaap.services import JWTService, MinioStorage


@pytest.fixture(autouse=True)
def disable_cache_for_tests():
    with override_settings(
        CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
    ):
        yield


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="session")
def jwt_service() -> JWTService:
    return JWTService(secret_key=settings.JWT_SECRET)


@pytest.fixture
def storage() -> Generator[MinioStorage, None, None]:
    client = minio.Minio(
        endpoint=settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_USER,
        secret_key=settings.MINIO_PASSWORD,
        secure=False,
    )
    minio_storage = MinioStorage(client=client)
    if not client.bucket_exists("test-bucket"):
        client.make_bucket("test-bucket")
    yield minio_storage
    for obj in client.list_objects("test-bucket", recursive=True):
        assert obj.object_name is not None
        client.remove_object("test-bucket", obj.object_name)


@pytest.fixture
def sample_doc(storage: MinioStorage) -> Document:
    file_uuid = uuid.uuid4()
    name = f"{file_uuid.hex}.txt"
    file = io.BytesIO(b"original content")
    size = len(file.getbuffer())
    result = storage.upload(file=file, bucket="test-bucket", name=name, size=size)
    return Document.objects.create(
        uuid=file_uuid,
        bucket="test-bucket",
        name=name,
        size=size,
        mimetype="text/plain",
        etag=result["etag"],
        logs={"uploaded_by": "original-user"},
    )


@pytest.fixture
def creds() -> dict:
    return {
        "normal": {"username": "normal", "password": "normal"},
        "staff": {"username": "staff", "password": "staff"},
        "admin": {"username": "admin", "password": "admin"},
    }


@pytest.fixture
def dct() -> ContentType:
    return ContentType.objects.get(app_label="docs", model="document")


@pytest.fixture
def rdp(dct: ContentType) -> Permission:
    return Permission.objects.get(content_type=dct, codename="read_document")


@pytest.fixture
def wdp(dct: ContentType) -> Permission:
    return Permission.objects.get(content_type=dct, codename="write_document")


@pytest.fixture
def ddp(dct: ContentType) -> Permission:
    return Permission.objects.get(content_type=dct, codename="delete_document")


@pytest.fixture
def normal_group(rdp: Permission) -> Group:
    group = Group.objects.create(name="normal")
    group.permissions.set([rdp])
    return group


@pytest.fixture
def normal_user(creds: dict, normal_group: Group) -> User:
    normal = User.objects.create_user(**creds["normal"])
    normal.groups.add(normal_group)
    return normal


@pytest.fixture
def staff_group(rdp: Permission, wdp: Permission) -> Group:
    group, _ = Group.objects.get_or_create(name="staff")
    group.permissions.set([rdp, wdp])
    return group


@pytest.fixture
def staff_user(creds: dict, staff_group: Group) -> User:
    staff = User.objects.create_user(**creds["staff"])
    staff.groups.add(staff_group)
    return staff


@pytest.fixture
def admin_group(rdp: Permission, wdp: Permission, ddp: Permission) -> Group:
    group = Group.objects.create(name="admin")
    group.permissions.set([rdp, wdp, ddp])
    return group


@pytest.fixture
def admin_user(creds: dict, admin_group: Group) -> User:
    admin = User.objects.create_user(**creds["admin"])
    admin.groups.add(admin_group)
    return admin


@pytest.fixture
def admin_token(admin_user, api_client: APIClient, creds: dict) -> str:
    url = reverse("login")
    resp = api_client.post(url, data=creds["admin"])
    return resp.data["access_token"]


@pytest.fixture
def normal_token(normal_user, api_client: APIClient, creds: dict) -> str:
    url = reverse("login")
    resp = api_client.post(url, data=creds["normal"])
    return resp.data["access_token"]


@pytest.fixture
def staff_token(staff_user, api_client: APIClient, creds: dict) -> str:
    url = reverse("login")
    resp = api_client.post(url, data=creds["staff"])
    return resp.data["access_token"]
