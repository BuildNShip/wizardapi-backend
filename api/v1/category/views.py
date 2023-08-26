import json

from api.exception import InvalidPK
from .serializers import CategorySerializer, CategoryListSerializer
from apps.category.models import Category
from apps.app_settings.models import ResponseCodes
from rest_framework.views import APIView
from rest_framework.response import Response
from api.utility.utils import CustomResponse, Utils
from ...backends import JWTAuthentication


class CategoryListView(APIView):
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
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        page = request.query_params.get("pageIndex", 1)
        per_page = request.query_params.get("perPage", None)
        filter_query = request.query_params.get("query", "")
        kwargs = {"category_name__icontains": filter_query, "deleted_at__isnull": True,
                  "status": Category.ACTIVE} if filter_query != "" else {"deleted_at__isnull": True,
                                                                         "status": Category.ACTIVE}

        queryset = Category.objects.filter(**kwargs)
        pagination = Utils.pagination(queryset, page, per_page)
        serializer = CategoryListSerializer(pagination.get("queryset"), many=True)

        return CustomResponse.success({"list": serializer.data, "pagination": pagination.get("pagination")})


class CategoryCreateUpdateView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            request_data = json.loads(json.dumps(request.data))
            print("request",request_data)
            post_fields = {
                "category_name": "categoryName"
            }
            validate_data = Utils.get_input(request, post_fields, request_data)
            print("validated data",validate_data)

            pk = Utils.get_pk(request_data)
            print("pk",pk)

            if pk:
                instance = Category.objects.get(pk=pk, deleted_at__isnull=True)
                serializer = CategorySerializer(instance, data=validate_data, context={"request": request})
            else:
                serializer = CategorySerializer(data=validate_data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return CustomResponse.success(message="Category updated successfully" if pk else
                "Category created successfully")

            else:

                return CustomResponse.failure(error_code=1001, message="validation error",
                                              debug_message="validation error",
                                              errors=serializer.errors)
        except Category.DoesNotExist as dne:
            err = "Given pk value not exists or it might be removed"
            # ErrorReporting.error_report("NO_DATA", "MEDIUM", CategoryCreateUpdateView.__name__, err,
            #                                     request=request)
            return CustomResponse.failure(error_code=1002, message="Category not exists.", debug_message=str(dne))

        except InvalidPK as ipk:
            return CustomResponse.failure(error_code=ipk.errors.get("error_code"), message=str(ipk),
                                          debug_message=ipk.errors.get("message"))

        except Exception as e:
            import traceback
            # ErrorReporting.error_report("EXCEPTION", "HIGH", CategoryCreateUpdateView.__name__,
            #                                     traceback.format_exc(), request=request)
            return CustomResponse.failure(error_code=1002, message="exception caught", debug_message=str(e))
