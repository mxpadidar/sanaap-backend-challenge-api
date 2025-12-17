from django.conf import settings
from rest_framework import serializers

from sanaap.docs.models import Document


class HealthResp(serializers.Serializer):
    detail = serializers.CharField()


class SignupReq(serializers.Serializer):
    username = serializers.CharField(max_length=150, allow_blank=False)
    password = serializers.CharField(max_length=128, allow_blank=False, write_only=True)
    email = serializers.EmailField(max_length=254, allow_blank=True, required=False)
    first_name = serializers.CharField(max_length=30, allow_blank=True, required=False)
    last_name = serializers.CharField(max_length=150, allow_blank=True, required=False)


class SignupResp(serializers.Serializer):
    detail = serializers.CharField()


class LoginReq(serializers.Serializer):
    username = serializers.CharField(max_length=150, allow_blank=False)
    password = serializers.CharField(max_length=128, allow_blank=False, write_only=True)


class LoginResp(serializers.Serializer):
    access_token = serializers.CharField()


class FileReq(serializers.Serializer):
    file = serializers.FileField()

    def get_file_info(self):
        file = self.validated_data.get("file")
        return {
            "name": file.name,
            "ext": self._get_ext(file.name),
            "size": file.size,
            "mimetype": file.content_type,
        }

    def _get_ext(self, filename: str) -> str:
        parts = filename.split(".")
        if len(parts) < 2 or not parts[-1]:
            raise serializers.ValidationError("Filename does not have an extension")
        return parts[-1].lower()


class DocResp(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:  # type: ignore
        model = Document
        fields = (
            "uuid",
            "name",
            "size",
            "mimetype",
            "status",
            "created_at",
            "updated_at",
            "url",
        )
        read_only_fields = fields

    def get_url(self, obj) -> str | None:
        storage = self.context.get("storage")
        if storage is None:
            return None
        return storage.get_url(
            bucket=obj.bucket, name=obj.name, ttl=settings.MINIO_URL_TTL
        )
