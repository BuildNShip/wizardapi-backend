import json
from urllib import response
from rest_framework.views import APIView

from api.utility.utils import CustomResponse
from apps.api_data.models import APIData, UserToken
from rest_framework.response import Response

class GetAPIResponseView(APIView):
    def post(self, request):
        # Extracting the API token from the URL
        url = request.path
        api_token, remaining_url = url.split('/test/', 1)[1].split('/', 1)
        print("api_token:", api_token)
        print("remaining_url:", remaining_url)
        usertoken=UserToken.objects.get(api_token=api_token)
        print("usertoken:", usertoken)

        api_data=APIData.objects.get(user_token=usertoken)
        print("api_data:", api_data)
        api_response = api_data.responses.through.objects.filter(api_data=api_data, default_response=True).first().api_response
        print("apidataaa",api_response)
        # api_response=api_data.responses.filter(default_response=True).first()
        if api_response is None:
            body=None
            response_code=200
        else:
            body=json.loads(json.dumps(api_response.body))
            print("body",body)
            print(type(body))
            response_code=api_response.response_code.code
            print("responsecode",response_code)
        return Response(body,status=response_code)





