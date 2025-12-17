from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sanaap import container, handlers
from sanaap.api import serializers


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
