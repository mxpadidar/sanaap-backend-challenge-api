import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from sanaap import exceptions

logger = logging.getLogger(__name__)

# Map custom exception types to HTTP status codes
EXC_STATUS_CODE: dict[type[exceptions.BaseExc], int] = {
    exceptions.ConflictExc: status.HTTP_409_CONFLICT,
}


def drf_exception_handler_override(exc: Exception, context: dict) -> Response | None:
    """Custom DRF exception handler for application-specific exceptions.

    This handles all exceptions inheriting from `BaseExc` and returns
    a structured response with the appropriate HTTP status code. Unknown
    exceptions are passed to DRF's default handler.
    """
    if isinstance(exc, exceptions.BaseExc):
        exc_type = type(exc)
        status_code = EXC_STATUS_CODE.get(exc_type)
        if status_code is None:
            logger.critical(
                f"Unmapped application exception caught: {exc_type.__name__}"
            )
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response({"detail": exc.detail}, status=status_code)

    return drf_exception_handler(exc, context)
