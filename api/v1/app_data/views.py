from .serializers import CodeSerializer
from apps.app_settings.models import ResponseCodes
from rest_framework.views import APIView
from rest_framework.response import Response

class ListResponseCode(APIView):
    """
    API view to retrieve a list of response codes.

    Endpoint: `/response-code/list/`

    HTTP Method: GET

    Request Parameters:
    - None

    Response:
    - Returns a list of response codes.
    
    Uses `ResponseCodes` model and `CodeSerializer` for serialization.

    Returns a JSON response containing serialized data.

    """

    def get(self):
        response_codes = ResponseCodes.objects.filter(deleted_at__isnull=True,status=ResponseCodes.ACTIVE)
        serializer = CodeSerializer(response_codes, many=True)
        return Response(serializer.data)