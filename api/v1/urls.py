from django.urls import include,path

urlpatterns = [
    path('category/', include('category.urls')),
]