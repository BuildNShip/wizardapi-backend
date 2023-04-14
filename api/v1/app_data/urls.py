from django.urls import include,path

from .views import ListResponseCode

urlpatterns = [
    path('response-code/list',ListResponseCode.as_view(), name="list_response_code")
]