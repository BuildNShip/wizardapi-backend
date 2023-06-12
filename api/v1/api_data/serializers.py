from apps.api_data.models import APIData, ApiResponses
from rest_framework import serializers

from apps.app_settings.models import ResponseCodes


class ApiResponsesSerializer(serializers.ModelSerializer):
    responseCode = serializers.PrimaryKeyRelatedField(queryset=ResponseCodes.objects.filter(deleted_at__isnull=True,
                                                                                            status=ResponseCodes.ACTIVE),
                                                      source='response_code')

    class Meta:
        model = ApiResponses
        fields = ["id", 'responseCode', 'body']


class UrlSerializer(serializers.ModelSerializer):
    responses = ApiResponsesSerializer(many=True, required=True)

    class Meta:
        model = APIData
        fields = ("id", "user_token", "responses", "url", "method", "responses", "category",
                  "created_by", "updated_by")

    def create(self, validated_data):
        responses = validated_data.pop("responses")

        api_data_obj = APIData.objects.create(**validated_data)
        if responses:
            for res_obj in responses:
                default = res_obj.pop('default')
                api_data_obj.responses.add(ApiResponses.objects.create(**res_obj),
                                           through_defaults={
                                               'default_response': default})

        return api_data_obj

    def update(self, instance, validated_data):
        responses = validated_data.pop("responses")

        super(UrlSerializer, self).update(instance, validated_data)
        if responses:
            instance.responses.clear()
            for res_obj in responses:
                default = res_obj.pop('default')
                if 'id' in res_obj.keys():
                    res_obj_id = res_obj.pop('id')
                    api_res_qst = ApiResponses.objects.filter(id=res_obj_id)
                    ApiResponses.objects.filter(id=res_obj_id).update(**res_obj)
                    api_res_obj = api_res_qst.first()
                else:
                    api_res_obj = ApiResponses.objects.create(**res_obj)
                instance.responses.add(api_res_obj,
                                       through_defaults={
                                           'default_response': default})

        return instance


class UrlListSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIData
        fields = ("id", "url", "category")


class UrlViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIData
        fields = ("id", "url", "method", "category")
