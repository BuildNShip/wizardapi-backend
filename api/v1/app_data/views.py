from .serializers import CodeSerializer
from apps.app_settings.models import ResponseCodes
from rest_framework.views import APIView
from api.utility.utils import CustomResponse, Utils
from ...backends import JWTAuthentication


class ResponseCodeListView(APIView):
    """
    API view to retrieve a list of response codes.

    Endpoint: `/response-code/list`

    HTTP Method: GET

    Request Parameters:
    - None

    Response:
    - Returns a list of response codes.

    Uses `ResponseCodes` model and `CodeSerializer` for serialization.

    Returns a JSON response containing serialized data.

    """
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        print(ResponseCodes.objects.all())
        page = request.query_params.get("pageIndex", 1)
        per_page = request.query_params.get("perPage", None)
        filter_query = request.query_params.get("query", "")
        kwargs = {"code__icontains": filter_query, "deleted_at__isnull": True,
                  "status": ResponseCodes.ACTIVE} if filter_query != "" else {"deleted_at__isnull": True,
                                                                           "status": ResponseCodes.ACTIVE}
        print(kwargs)
        queryset = ResponseCodes.objects.filter(**kwargs)
        pagination = Utils.pagination(queryset, page, per_page)
        serializer = CodeSerializer(pagination.get("queryset"), many=True)

        return CustomResponse.success({"list": serializer.data, "pagination": pagination.get("pagination")})