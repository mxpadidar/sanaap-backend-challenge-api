import minio
import punq
from django.conf import settings

from sanaap import services

container = punq.Container()

container.register(
    services.JWTService,
    instance=services.JWTService(secret_key=settings.JWT_SECRET),
)

container.register(
    minio.Minio,
    instance=minio.Minio(
        endpoint=settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_USER,
        secret_key=settings.MINIO_PASSWORD,
        secure=settings.MINIO_SSL,
    ),
)

container.register(
    services.MinioStorage,
    instance=services.MinioStorage(
        client=container.resolve(minio.Minio),  # type: ignore
    ),
)


def get_jwt_service() -> services.JWTService:
    return container.resolve(services.JWTService)  # type: ignore


def get_storage() -> services.MinioStorage:
    return container.resolve(services.MinioStorage)  # type: ignore
