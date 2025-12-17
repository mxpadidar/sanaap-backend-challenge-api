import uuid

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from sanaap.docs.enums import DocStatus
from sanaap.docs.models import Document

pytestmark = pytest.mark.django_db


@pytest.fixture
def url(sample_doc: Document) -> str:
    return reverse("doc-get-put-del", kwargs={"file_uuid": sample_doc.uuid})


def test_get_doc_detail_returns_200_for_normal_user(
    api_client: APIClient, normal_token: str, sample_doc: Document, url: str
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {normal_token}")
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["uuid"] == str(sample_doc.uuid)


def test_get_doc_detail_returns_401_without_auth(api_client: APIClient, url: str):
    response = api_client.get(url)
    assert response.status_code == 401


def test_get_doc_detail_returns_404_for_non_existing_uuid(
    api_client: APIClient, admin_token: str
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    url = reverse("doc-get-put-del", kwargs={"file_uuid": uuid.uuid4()})
    response = api_client.get(url)
    assert response.status_code == 404


def test_get_doc_detail_returns_404_for_deleted_doc(
    api_client: APIClient, admin_token: str, sample_doc: Document, url: str
):
    sample_doc.status = DocStatus.DELETED
    sample_doc.save(update_fields=["status"])

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.get(url)

    assert response.status_code == 404
