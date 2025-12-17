import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from sanaap.docs.models import Document

pytestmark = pytest.mark.django_db


@pytest.fixture
def url() -> str:
    return reverse("doc-post-list")


def test_get_doc_list_returns_200_for_normal(
    api_client: APIClient, normal_token: str, url: str
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {normal_token}")
    response = api_client.get(url)
    assert response.status_code == 200
    assert "results" in response.data


def test_get_doc_list_returns_401_without_auth(api_client: APIClient, url: str):
    response = api_client.get(url)
    assert response.status_code == 401


def test_get_doc_list_filters_by_name(
    api_client: APIClient, admin_token: str, url: str, sample_doc: Document
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")

    response = api_client.get(url, {"name": sample_doc.name[:3]})
    assert response.status_code == 200
    assert len(response.data["results"]) == 1

    response = api_client.get(url, {"name": "no-match"})
    assert response.status_code == 200
    assert response.data["results"] == []


@pytest.mark.usefixtures("sample_doc")
def test_get_doc_list_pagination_structure(
    api_client: APIClient, admin_token: str, url: str
):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = api_client.get(url)

    assert response.status_code == 200
    assert set(response.data.keys()) == {"count", "next", "previous", "results"}
    assert response.data["count"] == 1
