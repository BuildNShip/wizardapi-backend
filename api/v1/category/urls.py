from django.urls import path
from .views import AddEditCategory, ListCategory

urlpatterns = [
    path('category/list', ListCategory.as_view(), name="list_category"),
    path('category/edit', AddEditCategory.as_view(), name="add_edit_category"),
    path('category/edit/<int:category_id>', AddEditCategory.as_view(), name="add_edit_category"),
]