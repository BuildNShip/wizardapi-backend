from .serializers import CategorySerializer
from apps.category.models import Category
from apps.app_settings.models import ResponseCodes
from rest_framework.views import APIView
from rest_framework.response import Response

class ListCategory(APIView):
    """
    API view to retrieve a list of active categories.

    Endpoint: `/category/list/`

    HTTP Method: GET

    Request Parameters:
    - None

    Response:
    - Returns a list of active categories.
    
    Uses `Category` model and `CategorySerializer` for serialization.

    Returns a JSON response containing serialized category data.

    """
    def get(self):
        categories=Category.objects.filter(deleted_at__isnull=True,status=ResponseCodes.ACTIVE)
        serializer=CategorySerializer(categories, many=True)
        return Response(serializer.data)

class AddEditCategory(APIView):
    def post(self,request):
        request_data=request.data
        serializer=CategorySerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"hasError": True})
    
    def put(self,request,category_id):
        category=Category.objects.get(id=category_id)
        request_data=request.data
        serializer=CategorySerializer(category,data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"hasError": True})


