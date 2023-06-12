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
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            msg = {
                "hasError": True,
                "errorCode": 2001,
                "message": "Invalid Token [ERR:2001]",
                "debugMessage": "",
                "response": None
            }
            raise CustomAPIException(msg)

        if len(auth_header) == 1:
            msg = {
                "hasError": True,
                "errorCode": 2002,
                "message": "Invalid Token [ERR:2002]",
                "debugMessage": "",
                "response": None
            }
            raise CustomAPIException(msg)

        elif len(auth_header) > 2:
            msg = {
                "hasError": True,
                "errorCode": 2003,
                "message": "Invalid Token [ERR:2003]",
                "debugMessage": "",
                "response": None
            }
            raise CustomAPIException(msg)

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
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
                user_id = payload.get("user_id", None)
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
                        response = CommonAuthResourceAccess.verify_auth_token(token)
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
                            user_token_obj = UserToken.objects.filter(deleted_at__isnull=True, status=UserToken.ACTIVE,
                                                                      user_token=payload.get('userToken')).first()
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
            msg = {
                "hasError": True,
                "errorCode": 2009,
                "message": "Invalid Token [ERR:2009]",
                "debugMessage": "",
                "response": None
            }
            raise CustomAPIException(msg)


