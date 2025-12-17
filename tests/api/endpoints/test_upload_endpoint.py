import io

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def url() -> str:
    return reverse("doc-post-list")  # POST usually goes to the list endpoint


@pytest.fixture
def payload() -> dict:
    f = io.BytesIO(b"new upload content")
    f.name = "new_file.txt"
    return {"file": f}


def test_upload_doc_returns_201_for_admin(
    api_client: APIClient, admin_token: str, url: str, payload: dict
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.post(url, data=payload, format="multipart")

    assert response.status_code == 201
    assert "uuid" in response.data
    assert "name" in response.data
    assert "mimetype" in response.data
    assert "size" in response.data


def test_upload_doc_returns_201_for_staff(
    api_client: APIClient, staff_token: str, url: str, payload: dict
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {staff_token}")
    response = api_client.post(url, data=payload, format="multipart")

    assert response.status_code == 201
    assert "uuid" in response.data


def test_upload_doc_returns_403_for_normal(
    api_client: APIClient, normal_token: str, url: str, payload: dict
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {normal_token}")
    response = api_client.post(url, data=payload, format="multipart")
    assert response.status_code == 403


def test_upload_doc_returns_401_without_auth(
    api_client: APIClient, url: str, payload: dict
):
    response = api_client.post(url, data=payload, format="multipart")
    assert response.status_code == 401


def test_upload_doc_requires_file_field(
    api_client: APIClient, admin_token: str, url: str
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.post(url, data={}, format="multipart")
    assert response.status_code == 400
    assert "file" in response.data
