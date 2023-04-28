from django.urls import path
from .views import (UrlCreateUpdateView, UrlDetailView, UrlListView)

urlpatterns = [
    path('url/list', UrlListView.as_view(), name="url_list"),
    path('url/view', UrlDetailView.as_view(), name="url_detail_view"),
    path('url/update', UrlCreateUpdateView.as_view(), name="url_create_update"),

]