import functools
import secrets
from typing import Literal

from django.core.management.utils import get_random_secret_key
from pydantic_settings import BaseSettings, SettingsConfigDict


class Envs(BaseSettings):
    environment: Literal["dev", "prod"] = "dev"

    django_secret: str = get_random_secret_key()
    django_allowed_hosts: list[str] = ["*"]

    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "postgres"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    minio_root_user: str = "minio"
    minio_root_password: str = "minio"
    minio_endpoint: str = "localhost:9000"
    minio_ssl: bool = False

    redis_host: str = "localhost"
    redis_port: int = 6379

    jwt_secret: str = secrets.token_hex(32)
    jwt_ttl_sec: int = 600

    model_config = SettingsConfigDict(env_file=".env", frozen=True)


@functools.cache
def get_envs() -> Envs:
    return Envs()
