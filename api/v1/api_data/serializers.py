from apps.api_data.models import APIData
from rest_framework import serializers

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model= APIData
        fields=("id","api_token", "user_token", "url", "method", "category", "created_by", "updated_by")

class UrlListSerializer(serializers.ModelSerializer):
    class Meta:
        model= APIData
        fields=("id", "url", "category")

class UrlViewSerializer(serializers.ModelSerializer):
    class Meta:
        model= APIData
        fields=("id", "url", "method", "category")