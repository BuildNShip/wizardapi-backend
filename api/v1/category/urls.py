from django.urls import path
from .views import (CategoryCreateUpdateView, CategoryListView)

urlpatterns = [
    path('category/list', CategoryListView.as_view(), name="category_list"),
    # path('category/edit', AddEditCategory.as_view(), name="add_edit_category"),
    # path('category/edit/<int:category_id>', AddEditCategory.as_view(), name="add_edit_category"),
    path('category/update', CategoryCreateUpdateView.as_view(), name="category_create_update"),

]