from rest_framework import serializers


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, allow_blank=False)
    password = serializers.CharField(max_length=128, allow_blank=False, write_only=True)
    email = serializers.EmailField(max_length=254, allow_blank=True, required=False)
    first_name = serializers.CharField(max_length=30, allow_blank=True, required=False)
    last_name = serializers.CharField(max_length=150, allow_blank=True, required=False)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, allow_blank=False)
    password = serializers.CharField(max_length=128, allow_blank=False, write_only=True)
