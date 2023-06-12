from django.urls import include, path, re_path

from api.v1.views import GetAPIResponseView

urlpatterns = [
    path('category/', include('api.v1.category.urls')),
    path('app-data/', include('api.v1.app_data.urls')),
    path('api-data/', include('api.v1.api_data.urls')),

    re_path('test/.*', GetAPIResponseView.as_view(), name="get_api_response"),

]