from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """API view to check the health of the application."""

    def get(self, request):
        return Response(
            {"detail": "ok"},
            status=status.HTTP_200_OK,
        )
