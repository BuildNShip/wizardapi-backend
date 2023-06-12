from django.urls import path
from .views import (CategoryCreateUpdateView, CategoryListView)

urlpatterns = [
    path('list', CategoryListView.as_view(), name="category_list"),
    path('update', CategoryCreateUpdateView.as_view(), name="category_create_update"),

]