
import json
from api.exception import InvalidPK
from apps.api_data.models import APIData
from .serializers import CategorySerializer, CategoryListSerializer, UrlListSerializer, UrlSerializer, UrlViewSerializer
from apps.category.models import Category
from apps.app_settings.models import ResponseCodes
from rest_framework.views import APIView
from rest_framework.response import Response
from api.utility.utils import CustomResponse, Utils


class UrlListView(APIView):
    """
    API view to retrieve a list of active urls.

    Endpoint: `/url/list/`

    HTTP Method: GET

    Request Parameters:
    - None

    Response:
    - Returns a list of active urls.
    
    Uses `APIData` model and `UrlListSerializer` for serialization.

    Returns a JSON response containing serialized url data.

    """
    def get(self,request):
        page = request.query_params.get("pageIndex", 1)
        per_page = request.query_params.get("perPage", None)
        filter_query =  request.query_params.get("query", "")
        kwargs = {"url__icontains": filter_query, "deleted_at__isnull": True,
         "status": APIData.ACTIVE} if filter_query != "" else {"deleted_at__isnull": True,
         "status": APIData.ACTIVE}
        
        queryset=APIData.objects.filter(**kwargs)
        pagination = Utils.pagination(queryset, page, per_page)
        serializer=UrlListSerializer(pagination.get("queryset"), many=True)

        return CustomResponse.success({"list": serializer.data, "pagination": pagination.get("pagination")})


class UrlDetailView(APIView):
    """
    API view to retrieve a specific APIData object.

    Endpoint: `/url/view/<int:pk>/`

    HTTP Method: GET

    Request Parameters:
    - pk (int): The primary key of the APIData object to retrieve.

    Response:
    - Returns the APIData object with the given primary key.

    Uses `APIData` model and `UrlViewSerializer` for serialization.

    Returns a JSON response containing serialized APIData object data.
    """
    def post(self, request):
        try:
            pk = request.data.get('pk')
            instance = APIData.objects.get(pk=pk, deleted_at__isnull=True)
            serializer = UrlViewSerializer(instance, context={"request": request})
            return CustomResponse.success(serializer.data)
        except APIData.DoesNotExist:
            return CustomResponse.failure(error_code=1002, message="Url not found.")



class UrlCreateUpdateView(APIView):

    def post(self,request):
        try:
            request_data = json.loads(json.dumps(request.data))
            post_fields = {
                "url": "url",
                "method": "method",
                "category": "category",
                "body":"body"
            }
            validate_data = Utils.get_input(request, post_fields, request_data)
            pk = Utils.get_pk(request_data)
            if pk:
                instance = APIData.objects.get(pk=pk, deleted_at__isnull=True)
                serializer = UrlSerializer(instance, data=validate_data, context={"request": request})
            else:
                serializer = UrlSerializer(data=validate_data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return CustomResponse.success(message="Url updated successfully" if pk else
                "Url created successfully")

            else:

                return CustomResponse.failure(error_code=1001, message="validation error", debug_message="validation error",
                                        errors=serializer.errors)
        except APIData.DoesNotExist as dne:
            err = "Given pk value not exists or it might be removed"
            # ErrorReporting.error_report("NO_DATA", "MEDIUM", CategoryCreateUpdateView.__name__, err,
            #                                     request=request)
            return CustomResponse.failure(error_code=1002, message="Url not exists.", debug_message=str(dne))

        except InvalidPK as ipk:
            return CustomResponse.failure(error_code=ipk.errors.get("error_code"), message=str(ipk),
                                    debug_message=ipk.errors.get("message"))

        except Exception as e:
            import traceback
            # ErrorReporting.error_report("EXCEPTION", "HIGH", CategoryCreateUpdateView.__name__,
            #                                     traceback.format_exc(), request=request)
            return CustomResponse.failure(error_code=1002, message="exception caught", debug_message=str(e))







