from django.urls import path

from sanaap.api import views

urlpatterns = [
    path("health/", views.HealthCheckView.as_view(), name="health-check"),
]
