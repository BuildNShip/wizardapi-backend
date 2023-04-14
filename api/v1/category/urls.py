from django.urls import path
from .views import ListCategory

urlpatterns = [
    path('category/list', ListCategory.as_view(), name="list_category")
]