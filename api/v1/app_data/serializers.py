from apps.app_settings.models import ResponseCodes
from rest_framework import serializers

class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseCodes
        fields = ('id', 'code', 'title')