from django.conf import settings
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import parsers, status
from rest_framework.decorators import parser_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from sanaap import container, handlers
from sanaap.api import permissions, serializers
from sanaap.api.auth import TokenAuth
from sanaap.docs.enums import DocStatus
from sanaap.docs.models import Document


class HealthCheckView(APIView):
    serializer_class = serializers.HealthResp

    def get(self, request):
        return Response(data={"detail": "ok"}, status=status.HTTP_200_OK)


class SignupView(APIView):
    @extend_schema(request=serializers.SignupReq, responses={201: serializers.SignupResp})
    def post(self, request):
        serializer = serializers.SignupReq(data=request.data)
        serializer.is_valid(raise_exception=True)
        handlers.handle_user_signup(default_group="normal", **serializer.validated_data)
        return Response(
            data=serializers.SignupResp({"detail": "User created."}).data,
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    @extend_schema(request=serializers.LoginReq, responses={200: serializers.LoginResp})
    def post(self, request):
        serializer = serializers.LoginReq(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = handlers.handle_user_login(
            jwt_service=container.get_jwt_service(),
            token_ttl=settings.JWT_TTL,
            **serializer.validated_data,
        )
        return Response(
            data=serializers.LoginResp({"access_token": token}).data,
            status=status.HTTP_200_OK,
        )


class DocsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "limit"
    max_page_size = 100


class DocPostListView(APIView):
    authentication_classes = [TokenAuth]

    def get_permissions(self) -> list:
        if self.request.method == "POST":
            return [permissions.CanWriteDoc()]
        if self.request.method == "GET":
            return [permissions.CanReadDoc()]
        return [permissions.CanDeleteDoc()]  # just admin

    @parser_classes([parsers.MultiPartParser])
    @extend_schema(request=serializers.FileReq, responses={201: serializers.DocResp})
    def post(self, request):
        serializer = serializers.FileReq(data=request.data)
        serializer.is_valid(raise_exception=True)
        storage = container.get_storage()
        doc = handlers.handle_document_upload(
            storage=storage,
            username=request.user.username,  # type: ignore
            bucket=settings.DOCS_BUCKET,
            file=serializer.validated_data["file"],
            **serializer.get_file_info(),
        )
        return Response(
            serializers.DocResp(doc, context={"storage": storage}).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        parameters=[
            OpenApiParameter("name", type=OpenApiTypes.STR, required=False),
            OpenApiParameter("mimetype", type=OpenApiTypes.STR, required=False),
            OpenApiParameter("ordering", type=OpenApiTypes.STR, required=False),
            OpenApiParameter("page", type=OpenApiTypes.INT, required=False),
            OpenApiParameter("limit", type=OpenApiTypes.INT, required=False),
        ],
        responses=serializers.DocResp(many=True),
    )
    def get(self, request):
        qs = Document.objects.filter(status=DocStatus.ACTIVE)
        name = request.query_params.get("name")
        mimetype = request.query_params.get("mimetype")
        if name:
            qs = qs.filter(name__icontains=name)
        if mimetype:
            qs = qs.filter(mimetype=mimetype)
        ordering = request.query_params.get("ordering", "-created_at")
        qs = qs.order_by(*ordering.split(","))
        paginator = DocsPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.DocResp(page, many=True)
        return paginator.get_paginated_response(serializer.data)
        return [permissions.CanDeleteDoc()]  # just admin has this perm
