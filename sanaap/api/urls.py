from django.urls import path

from sanaap.api import views

urlpatterns = [
    path("health/", views.HealthCheckView.as_view(), name="health-check"),
    path("auth/signup/", views.SignupView.as_view(), name="signup"),
    path("auth/login/", views.LoginView.as_view(), name="login"),
    path("docs/", views.DocPostListView.as_view(), name="doc-post-list"),
    path(
        "docs/<uuid:file_uuid>/", views.DocGetPutDelView.as_view(), name="doc-get-put-del"
    ),
]
