from datetime import timedelta
from pathlib import Path

from .envs import get_envs

_envs = get_envs()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = _envs.django_secret

DEBUG = _envs.environment == "dev"

ALLOWED_HOSTS = _envs.django_allowed_hosts

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sanaap.core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

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

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # keep default Django loggers
    "formatters": {
        "standard": {"format": "[%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "standard"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "sanaap.api.exc_handler.drf_exception_handler_override"
}

JWT_SECRET = _envs.jwt_secret
JWT_TTL = timedelta(seconds=_envs.jwt_ttl_sec)

MINIO_USER = _envs.minio_root_user
MINIO_PASSWORD = _envs.minio_root_password
MINIO_ENDPOINT = _envs.minio_endpoint
MINIO_SSL = _envs.minio_ssl
