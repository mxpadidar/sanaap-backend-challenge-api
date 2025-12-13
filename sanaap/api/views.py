from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sanaap import handlers, services
from sanaap.api import serializers
from sanaap.container import container


class HealthCheckView(APIView):
    """API view to check the health of the application."""

    def get(self, request):
        return Response(
            {"detail": "ok"},
            status=status.HTTP_200_OK,
        )


class UserSignupView(APIView):
    def post(self, request):
        serializer = serializers.SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = handlers.handle_user_signup(**serializer.validated_data)
        return Response(
            data={"detail": "user created."},
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(APIView):
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = handlers.handle_user_login(
            jwt_service=container.resolve(services.JWTService),  # type: ignore
            token_ttl=settings.JWT_TTL,
            **serializer.validated_data,
        )
        return Response(
            data={"access_token": token},
            status=status.HTTP_200_OK,
        )
