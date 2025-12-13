import punq
from django.conf import settings

from sanaap import services

container = punq.Container()


container.register(
    services.JWTService,
    instance=services.JWTService(secret_key=settings.JWT_SECRET),
)
