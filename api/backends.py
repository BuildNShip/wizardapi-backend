import hashlib
import hmac

import jwt
from decouple import config
from django.conf import settings
from django.utils import timezone
from jwt.exceptions import InvalidSignatureError
from rest_framework import authentication
from datetime import datetime
from api.exception import CustomAPIException
from api.service import CommonAuthResourceAccess
from apps.api_data.models import UserToken


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        # print(request)

        request.user = None
        # print("user",request.user)
        auth_header = authentication.get_authorization_header(request).split()
        # print("auth header",auth_header)
        auth_header_prefix = self.authentication_header_prefix.lower()
        # print("auth header prefix",auth_header_prefix)


        if not auth_header:
            print("1")
            msg = {
                "hasError": True,
                "errorCode": 2001,
                "message": "Invalid Token [ERR:2001]",
                "debugMessage": "",
                "response": None
            }
            raise CustomAPIException(msg)

        if len(auth_header) == 1:
            print("2")

            msg = {
                "hasError": True,
                "errorCode": 2002,
                "message": "Invalid Token [ERR:2002]",
                "debugMessage": "",
                "response": None
            }
            raise CustomAPIException(msg)

        elif len(auth_header) > 2:
            print("3")

            msg = {
                "hasError": True,
                "errorCode": 2003,
                "message": "Invalid Token [ERR:2003]",
                "debugMessage": "",
                "response": None
            }
            raise CustomAPIException(msg)

        prefix = auth_header[0].decode('utf-8')
        print("prefix",prefix)
        token = auth_header[1].decode('utf-8')
        print("token",token)


        if prefix.lower() != auth_header_prefix:
            print('here')
            msg = {
                "hasError": True,
                "errorCode": 2004,
                "message": "Invalid Token [ERR:2004]",
                "debugMessage": "",
                "response": None
            }
            raise CustomAPIException(msg)

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=['HS256'], options={"verify_signature": True})
            if payload:
                user_id = payload.get("userId", None)
                expiry_date = payload.get("expiry", None)

                if expiry_date:
                    now = timezone.now().replace(tzinfo=None)
                    expiry_on = datetime.strptime(expiry_date, "%Y-%m-%d %H:%M:%S")
                    if expiry_on < now:
                        msg = {
                            "hasError": True,
                            "errorCode": 2006,
                            "message": "Token Expired [ERR:2006]",
                            "debugMessage": "",
                            "response": None
                        }
                        raise CustomAPIException(msg)
                    else:
                        response = CommonAuthResourceAccess().verify_auth_token(token)
                        print(response,token)
                        if response.get('hasError'):
                            msg = {
                                    "hasError": True,
                                    "errorCode": response.get('errorCode'),
                                    "message": f"Authentication Failed [ERR:{response.get('errorCode')}]",
                                    "debugMessage": "",
                                    "response": ""
                                }
                            raise CustomAPIException(msg)

                        # if payload.get("secretToken", "") != user_obj.access_secret_token:
                        #     msg = {
                        #         "hasError": True,
                        #         "errorCode": 2020,
                        #         "message": 'Session has been expired.',
                        #         "debugMessage": "",
                        #         "response": ""
                        #     }
                        #     raise CustomAPIException(msg)

                        else:
                            user_token_obj,created = UserToken.objects.get_or_create(deleted_at=None, status=UserToken.ACTIVE,
                                                                      user_token=response.get('response').get('app_token'))
                            return user_id, user_token_obj
                else:
                    msg = {
                        "hasError": True,
                        "errorCode": 2008,
                        "message": "Token Expired [ERR:2008]",
                        "debugMessage": "",
                        "response": None
                    }
                    raise CustomAPIException(msg)



            else:
                err = "jwt payload is empty"
                # ErrorReportingModel.error_report("WARNING", "MEDIUM", JWTAuthentication.__name__, err)
                msg = {
                    "hasError": True,
                    "errorCode": 2007,
                    "message": "Invalid Token [ERR:2007]",
                    "debugMessage": "",
                    "response": None
                }
                raise CustomAPIException(msg)

        except InvalidSignatureError as ise:
            print(ise)
            msg = {
                "hasError": True,
                "errorCode": 2009,
                "message": "Invalid Token [ERR:2009]",
                "debugMessage": "",
                "response": None
            }
            raise CustomAPIException(msg)


