from api.helpers import generate_unique_api_token
from api.utility.utils import Utils
from apps.api_data.models import APIData, ApiDataResponses, ApiResponses
from rest_framework import serializers
from django.core.exceptions import ValidationError
from apps.app_settings.models import ResponseCodes


class ApiResponsesSerializer(serializers.ModelSerializer):
    responseCode = serializers.PrimaryKeyRelatedField(queryset=ResponseCodes.objects.filter(deleted_at__isnull=True,
                                                                                            status=ResponseCodes.ACTIVE),
                                                      source='response_code')
    default=serializers.SerializerMethodField()

    class Meta:
        model = ApiResponses
        fields = ["id", 'responseCode', 'body', 'default']

    def get_default(self, instance):
        # Retrieve the associated ApiDataResponses instance for the current ApiResponses instance
        api_data_response = instance.apidataresponses_set.filter(api_response=instance).first()

        if api_data_response:
            return api_data_response.default_response

        return None

class UrlSerializer(serializers.ModelSerializer):
    # responses = ApiResponsesSerializer(many=True, required=True)
    responses = serializers.JSONField()
    class Meta:
        model = APIData
        fields = ("id", "user_token", "url", "method", "responses", "category",
                 "created_at", "updated_at")

   

    # def validate_url(self, value):
    #     user_token = self.initial_data.get("user_token")

    #     if APIData.objects.filter(user_token=user_token, url=value).exists():

    #         if ApiDataResponses.objects.filter(api_data__user_token=user_token, api_data__url=value,default_response=True,).exists():
    #             raise serializers.ValidationError("An instance with the same user token and URL with default response already exists.")
            
    #     return value


    def create(self, validated_data):
        print("validated data serializer",validated_data)
        responses = validated_data.pop("responses")
        user_token=validated_data.get("user_token")
        print(user_token)
        if not user_token.api_token:
            user_token.api_token=generate_unique_api_token()
            user_token.save()

        
        api_data_obj = APIData.objects.create(**validated_data)
            
        if responses:
            print("responses",responses)
            for res_obj in responses:
                print(res_obj)
                post_fields={
                    'response_code':'responseCode',
                    'body':'body',
                    'default':'default'
                }
                new_res_obj = Utils.change_dict_keys(self.context.get('request'),post_fields,res_obj)
                print("responseobject",new_res_obj)
                response_code = new_res_obj.pop('response_code')
                print("responsecode",response_code)
                response_code_obj=ResponseCodes.objects.get(id=response_code)
                default = new_res_obj.pop('default')
                api_data_obj.responses.add(ApiResponses.objects.create(response_code=response_code_obj,**new_res_obj),
                                           through_defaults={
                                               'default_response': default})

        return api_data_obj

    def update(self, instance, validated_data):
        print("validated data edit serializer",validated_data)
        print("instance edit serializer",instance)

        responses = validated_data.pop("responses")

        super(UrlSerializer, self).update(instance, validated_data)
        if responses:
            instance.responses.clear()
            for res_obj in responses:
                print('resobj',res_obj)
                post_fields={
                    'response_code':'responseCode',
                    'body':'body',
                    'default':'default'
                }
                new_res_obj = Utils.change_dict_keys(self.context.get('request'),post_fields,res_obj)
                print("responseobject",new_res_obj)
                response_code = new_res_obj.pop('response_code')
                print("responsecode",response_code)
                response_code_obj=ResponseCodes.objects.get(id=response_code)
                default = res_obj.pop('default')

                if 'id' in res_obj.keys():
                    res_obj_id = res_obj.pop('id')
                    api_res_qst = ApiResponses.objects.filter(id=res_obj_id)
                    ApiResponses.objects.filter(id=res_obj_id).update(response_code=response_code_obj,**new_res_obj)
                    api_res_obj = api_res_qst.first()
                else:
                    print("entering")
                    api_res_obj = ApiResponses.objects.create(response_code=response_code_obj,**new_res_obj)
                instance.responses.add(api_res_obj,
                                       through_defaults={
                                           'default_response': default})

        return instance


class UrlListSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIData
        fields = ("id", "url", "category")


class UrlViewSerializer(serializers.ModelSerializer):
    responses = ApiResponsesSerializer(many=True,required=True) 
    class Meta:
        model = APIData
        fields = ("id", "url", "method", "category","responses")
