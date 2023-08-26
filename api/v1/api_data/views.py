import json
from api.exception import InvalidPK
from apps.api_data.models import APIData
from .serializers import UrlListSerializer, UrlSerializer, UrlViewSerializer
from rest_framework.views import APIView
from api.utility.utils import CustomResponse, Utils
from ...backends import JWTAuthentication
from decouple import config
import requests

class UrlListView(APIView):
    """
    API view to retrieve a list of active urls.

    Endpoint: `/url/list`

    HTTP Method: GET

    Request Parameters:
    - None

    Response:
    - Returns a list of active urls.
    
    Uses `APIData` model and `UrlListSerializer` for serialization.

    Returns a JSON response containing serialized url data.

    """
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        page = request.query_params.get("pageIndex", 1)
        per_page = request.query_params.get("perPage", None)
        filter_query = request.query_params.get("query", "")
        kwargs = {"url__icontains": filter_query, "deleted_at__isnull": True,
                  "status": APIData.ACTIVE} if filter_query != "" else {"deleted_at__isnull": True,
                                                                        "status": APIData.ACTIVE}

        queryset = APIData.objects.filter(**kwargs)
        pagination = Utils.pagination(queryset, page, per_page)
        serializer = UrlListSerializer(pagination.get("queryset"), many=True)

        return CustomResponse.success({"list": serializer.data, "pagination": pagination.get("pagination")})


class UrlDetailView(APIView):
    """
    API view to retrieve a specific APIData object.

    Endpoint: `url/view`

    HTTP Method: GET

    Request Parameters:
    - pk (int): The primary key of the APIData object to retrieve.

    Response:
    - Returns the APIData object with the given primary key.

    Uses `APIData` model and `UrlViewSerializer` for serialization.

    Returns a JSON response containing serialized APIData object data.
    """
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            pk = request.data.get('pk')
            print("pk",pk)
            instance = APIData.objects.get(pk=pk, deleted_at__isnull=True)
            print("instance",instance)
            serializer = UrlViewSerializer(instance, context={"request": request})
            print("data",serializer.data)
            return CustomResponse.success(serializer.data)
        except APIData.DoesNotExist:
            
            return CustomResponse.failure(error_code=1002, message="Url not found.")


class UrlCreateUpdateView(APIView):
    """

    params:{
    "url": string,
    "method": int,
    "category": int(fkey),
    "responses":{
    "responseCode":int(fkey),
    "body":json,
    "default":bool
    }
    }
    """
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            request_data = json.loads(json.dumps(request.data))
            print("request data", request_data)
            post_fields = {
                "url": "url",
                "method": "method",
                "category": "category",
                "responses": "responses"
            }
            validate_data = Utils.get_input(request, post_fields, request_data)
            print("validated data",validate_data)
            pk = Utils.get_pk(request_data)
            print("validated pk",pk)

            if pk:
                instance = APIData.objects.get(pk=pk, deleted_at__isnull=True)
                print("instance",instance)
                print("validateddata",validate_data)
                serializer = UrlSerializer(instance, data=validate_data, context={"request": request})
            else:
                serializer = UrlSerializer(data=validate_data, context={"request": request})
            if serializer.is_valid():
                api_obj = serializer.save()
                print("api",api_obj)
                base_url = config("BASE_URL")
                generated_url = base_url + '/' + api_obj.user_token.api_token + '/' + 'test/'+str(api_obj.url) 
                return CustomResponse.success({'url': generated_url}, message="Url updated successfully" if pk else "Url created successfully")

            else:

                return CustomResponse.failure(error_code=1001, message="validation error",
                                              debug_message="validation error",
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
            print(traceback.format_exc())
            # ErrorReporting.error_report("EXCEPTION", "HIGH", CategoryCreateUpdateView.__name__,
            #                                     traceback.format_exc(), request=request)
            return CustomResponse.failure(error_code=1002, message="exception caught", debug_message=str(e))
