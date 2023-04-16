from apps.category.models import Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields=("id","category_name", "user_token", "created_by", "updated_by")

class CategoryListSerializer(serializers.ModelSerializer):
    categoryName = serializers.CharField(source="category_name")

    class Meta:
        model= Category
        fields=("id","categoryName")