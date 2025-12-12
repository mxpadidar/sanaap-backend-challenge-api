from django.urls import reverse
from rest_framework.test import APIClient


def test_health_check_endpoint(api_client: APIClient):
    url = reverse("health-check")
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json() == {"detail": "ok"}
