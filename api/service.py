import json
import requests
import hmac
import hashlib
import time
from decouple import config


class CommonAuthAccessSignature:
    """
    Class for generating common auth Service API signature

    SIGNATURE_SECRET_KEY -> Should be same as the SECRET_KEY,
     used in common auth service for generating API signatures.
    """
    __secret_key = None

    def __init__(self):
        self.__secret_key = config("SIGNATURE_SECRET_KEY")

    def generate_signature(self):
        timestamp = int(time.time())
        signature_data = "API::" + config("ADMIN_URL") + "::POST::" + str(timestamp)
        signature = hmac.new(self.__secret_key.encode(), signature_data.encode(), hashlib.sha256).hexdigest()

        return timestamp, signature


class CommonAuthResourceAccess:
    """
        Class for Accessing common auth Service API's

    """

    URL = config("ADMIN_URL")

    END_POINTS = {
        "AUTH_TOKEN_VERIFY": "/api/verify-token",
    }
    
    def verify_auth_token(self, token):
        """
                function for Accessing common auth Service Authentication API.
        """
        json_data = {}
        try:
            print(self.URL)
            url = self.URL + self.END_POINTS.get("AUTH_TOKEN_VERIFY")

            timestamp, signature = CommonAuthAccessSignature().generate_signature()
            header = {
                "Content-Type": "application/json",
                "X-Signature": signature,
                "X-Timestamp": str(timestamp)
            }
            payload = {
                "token": token,
            }
            print(payload,signature,timestamp,url)
            result = requests.post(url, data=json.dumps(payload), headers=header)
            if result.status_code == 200:
                json_data = json.loads(result.text)
            # else:
            # ErrorReportingModel.error_report("NO_DATA", "HIGH", "get_resource", str(result))

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            # ErrorReportingModel.error_report("EXCEPTION", "HIGH", "get_resource", traceback.format_exc())

        return json_data
