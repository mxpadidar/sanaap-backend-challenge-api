import io
import uuid

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from sanaap.docs.models import Document

pytestmark = pytest.mark.django_db


@pytest.fixture
def url(sample_doc: Document) -> str:
    return reverse("doc-get-put-del", kwargs={"file_uuid": sample_doc.uuid})


@pytest.fixture
def payload() -> dict:
    f = io.BytesIO(b"new content")
    f.name = "updated_file.txt"
    return {"file": f}


def test_modify_doc_returns_200_for_admin(
    api_client: APIClient, admin_token: str, sample_doc: Document, url: str, payload: dict
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.put(url, data=payload, format="multipart")

    assert response.status_code == 200
    sample_doc.refresh_from_db()
    assert sample_doc.status == "modified"
    assert "modified_by" in sample_doc.logs
    assert sample_doc.logs["modified_by"] == "admin"


def test_modify_doc_returns_200_for_staff(
    api_client: APIClient, staff_token: str, sample_doc: Document, url: str, payload: dict
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {staff_token}")
    response = api_client.put(url, data=payload, format="multipart")

    assert response.status_code == 200
    sample_doc.refresh_from_db()
    assert sample_doc.status == "modified"
    assert sample_doc.logs["modified_by"] == "staff"


def test_modify_doc_returns_403_for_normal(
    api_client: APIClient, normal_token: str, url: str, payload: dict
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {normal_token}")
    response = api_client.put(url, data=payload, format="multipart")
    assert response.status_code == 403


def test_modify_doc_returns_401_without_auth(
    api_client: APIClient, url: str, payload: dict
):
    response = api_client.put(url, data=payload, format="multipart")
    assert response.status_code == 401


def test_modify_doc_returns_404_for_non_existing_uuid(
    api_client: APIClient, admin_token: str, payload: dict
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    url = reverse("doc-get-put-del", kwargs={"file_uuid": uuid.uuid4()})
    response = api_client.put(url, data=payload, format="multipart")
    assert response.status_code == 404


def test_modify_doc_requires_file_field(
    api_client: APIClient, admin_token: str, url: str
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.put(url, data={}, format="multipart")

    assert response.status_code == 400
    assert "file" in response.data
