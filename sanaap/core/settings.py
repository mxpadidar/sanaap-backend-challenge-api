from pathlib import Path

from .envs import get_envs

_envs = get_envs()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = _envs.django_secret

DEBUG = _envs.environment == "dev"

ALLOWED_HOSTS = _envs.django_allowed_hosts

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "rest_framework",
    "sanaap.api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sanaap.core.urls"

WSGI_APPLICATION = "sanaap.core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _envs.postgres_db,
        "USER": _envs.postgres_user,
        "PASSWORD": _envs.postgres_password,
        "HOST": _envs.postgres_host,
        "PORT": _envs.postgres_port,
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "sanaap.core.exc_handler.drf_exception_handler_override"
}

JWT_SECRET = _envs.jwt_secret
