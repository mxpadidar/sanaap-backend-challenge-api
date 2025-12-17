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


def test_delete_doc_endpoint_returns_204_on_valid_request(
    api_client: APIClient, sample_doc: Document, admin_token: str, url: str
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.delete(url)
    assert response.status_code == 204
    sample_doc.refresh_from_db()
    assert sample_doc.status == DocStatus.DELETED


def test_delete_doc_endpoint_returns_401_without_auth(api_client: APIClient, url: str):
    response = api_client.delete(url)
    assert response.status_code == 401


def test_delete_doc_endpoint_returns_403_without_admin_perm(
    api_client: APIClient, staff_token: str, url: str
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {staff_token}")
    response = api_client.delete(url)
    assert response.status_code == 403


def test_delete_doc_endpoint_returns_404_for_non_existing_uuid(
    api_client: APIClient, admin_token: str, url: str
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    url = reverse("doc-get-put-del", kwargs={"file_uuid": uuid.uuid4()})
    response = api_client.delete(url)
    assert response.status_code == 404
