import random
import secrets
import string
from django.db.models import Q
from django.conf import settings
from django.db.models.query import QuerySet
from api.exception import InvalidPK
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication
import jwt
from cryptography.fernet import Fernet

from apps.api_data.models import UserToken


class Encryption:
    key = Fernet(bytes(settings.ENCRYPT_KEY, 'utf-8'))

    def encrypt(self, content):
        try:
            encrypted_content = self.key.encrypt(str(content).encode('utf-8')).decode('utf-8')
            # for base64 encode
            # encrypted_content = self.key.encrypt(str(content).encode('ascii'))
            # b64_encoded_content = base64.urlsafe_b64encode(encrypted_content).decode('ascii')
            # return b64_encoded_content
            return encrypted_content
        except Exception as e:
            return None

    def decrypt(self, content):
        try:
            decrypted_content = self.key.decrypt(str(content).encode('utf-8')).decode('utf-8')

            # b64_decoded_content = base64.urlsafe_b64decode(content)
            # decrypted_content = self.key.decrypt(str(b64_decoded_content).decode('ascii'))
            return decrypted_content
        except Exception as e:
            return None


class Utils:
    @staticmethod
    def pagination(queryset: QuerySet, page=1, per_page=None):
        return_data = {
            "queryset": queryset,
            "pagination": {}
        }
        if not per_page:
            pagination_per_page = 10
            per_page = int(pagination_per_page) if pagination_per_page else settings.PAGE_SIZE
        if queryset:
            paginator = Paginator(queryset, per_page)
            try:
                queryset = paginator.page(page)
            except PageNotAnInteger:
                queryset = paginator.page(1)
            except EmptyPage:
                queryset = paginator.page(paginator.num_pages)

            return_data = {
                "queryset": queryset,
                "pagination": {
                    "count": paginator.count,
                    "totalPages": paginator.num_pages,
                    "isNext": queryset.has_next(),
                    "isPrev": queryset.has_previous(),
                    "nextPage": queryset.next_page_number() if queryset.has_next() else None
                }
            }

        return return_data

    @staticmethod
    def get_pk(data, key="id", cast=False):
        if key in data.keys():
            pk = data.get(key)
            if not cast:
                if isinstance(pk, int) and pk > 0:
                    return pk
                else:

                    raise InvalidPK("Unable to process the update",
                                    {"error_code": 1009, "message": f"Invalid primary key: {pk}"})
            else:
                if isinstance(pk, str):
                    return int(pk)
        else:

            return 0

    @staticmethod
    def get_input(request, post_fields: dict, request_data_set: list, who_did=True) -> dict:
        print(request.auth,request.user,"test")
        user_token = request.auth.id if request.auth else None

        if type(request_data_set) is list:
            for request_data in request_data_set:
                for key, value in post_fields.items():
                    if value in request_data.keys():
                        request_data[key] = request_data.pop(value)
                    else:
                        continue
                if who_did:
                    if request.auth:
                        if any(c in request_data.keys() for c in ('id', 'pk', 'ID')):
                            request_data.update({"updated_by": user_token,
                                                 "user_token": user_token})
                        else:
                            request_data.update({"updated_by": user_token, "created_by": user_token,
                                                 "user_token": user_token})
        else:
            for key, value in post_fields.items():
                if value in request_data_set.keys():
                    request_data_set[key] = request_data_set.pop(value)
                else:
                    continue
            if who_did:
                if request.auth:
                    if any(c in request_data_set.keys() for c in ('id', 'pk', 'ID')):
                        request_data_set.update({"updated_by": user_token, "user_token": user_token})
                    else:
                        request_data_set.update({"updated_by": user_token, "created_by": user_token,
                                                "user_token": user_token})
        print("requestdataset",request_data_set)
        return request_data_set

    @staticmethod
    def unique_id(model, field, length=5, prefix=""):
        model_obj = apps.get_model(model)
        unique_ref = ""
        not_unique = True
        while not_unique:
            unique_ref = prefix + str(random.randint(int("1" + "0" * (length - 1)), int("9" + "9" * (length - 1))))
            if not model_obj.objects.filter(**{field: unique_ref}):
                not_unique = False

        return unique_ref

    @staticmethod
    def generate_password():
        # define the alphabet
        letters = string.ascii_letters
        digits = string.digits
        special_chars = string.punctuation
        alphabet = letters + digits + special_chars
        # fix password length
        pwd_length = 8
        # generate a password string
        pwd = ''
        for i in range(pwd_length):
            pwd += ''.join(secrets.choice(alphabet))
        return pwd

    @staticmethod
    def change_dict_keys(request, post_fields: dict, request_data_set: list, who_did=True) -> dict:
        # validate_data = {} if type(request_data_set) is dict else []
        if type(request_data_set) is list:
            for request_data in request_data_set:
                for key, value in post_fields.items():
                    if value in request_data.keys():
                        request_data[key] = request_data.pop(value)
                    else:
                        continue
                if who_did:
                    if request.user:
                        if any(c in request_data.keys() for c in ('id', 'pk', 'ID')):
                            request_data.update({"updated_by": request.user.id})
                        else:
                            request_data.update({"updated_by": request.user.id, "created_by": request.user.id})
        else:
            for key, value in post_fields.items():
                if value in request_data_set.keys():
                    request_data_set[key] = request_data_set.pop(value)
                else:
                    continue
            if who_did:
                if request.user:
                    if any(c in request_data_set.keys() for c in ('id', 'pk', 'ID')):
                        request_data_set.update({"updated_by": request.user.id})
                    else:
                        request_data_set.update({"updated_by": request.user.id, "created_by": request.user.id})
        return request_data_set


class CustomResponse:
    """
    Class for returning custom success and faliure REST responses

    """

    @staticmethod
    def success(response={}, errors={}, message="Success", debug_message='', error_code=-1, status_code=None):
        json_obj = {"hasError": False, "errorCode": error_code, "message": message, "debugMessage": debug_message,
                    "response": response, 'errors': errors}
        if status_code is None:
            return Response(json_obj, status=status.HTTP_200_OK)
        return Response(json_obj, status=status_code)

    @staticmethod
    def failure(response={}, errors={}, debug_message='Invalid', status_code=None, error_code=1001,
                message="Failure"):
        json_obj = {"hasError": True, "errorCode": error_code, "message": message, "debugMessage": debug_message,
                    "response": response, 'errors': errors}
        if status_code is None:
            return Response(json_obj, status=status.HTTP_200_OK)
        return Response(json_obj, status_code)
