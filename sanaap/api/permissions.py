import logging
from typing import no_type_check

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class CanReadDoc(BasePermission):
    @no_type_check
    def has_permission(self, request: Request, view: APIView) -> bool:
        logger.info(request.user.username)
        return request.user.is_authenticated and request.user.has_perm(
            "docs.read_document"
        )


class CanWriteDoc(BasePermission):
    @no_type_check
    def has_permission(self, request: Request, view: APIView) -> bool:
        logger.info(request.user.username)
        return request.user.is_authenticated and request.user.has_perm(
            "docs.write_document"
        )


class CanDeleteDoc(BasePermission):
    @no_type_check
    def has_permission(self, request: Request, view: APIView) -> bool:
        logger.info(request.user.username)
        return request.user.is_authenticated and request.user.has_perm(
            "docs.delete_document"
        )
