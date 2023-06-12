from django.urls import include, path

from .views import ResponseCodeListView

urlpatterns = [
    path('response-code/list', ResponseCodeListView.as_view(), name="list_response_code")
]
