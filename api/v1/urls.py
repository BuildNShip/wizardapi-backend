from django.urls import include,path

urlpatterns = [
    path('category/', include('api.v1.category.urls')),
]