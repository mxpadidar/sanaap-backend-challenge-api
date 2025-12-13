from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sanaap import exceptions, handlers
from sanaap.api import serializers


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
        try:
            _ = handlers.handle_user_signup(**serializer.validated_data)
        except exceptions.ConflictExc as exc:
            return Response({"detail": exc.detail}, status=status.HTTP_409_CONFLICT)

        return Response(
            data={"detail": "user created."},
            status=status.HTTP_201_CREATED,
        )
