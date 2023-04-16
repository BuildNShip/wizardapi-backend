from rest_framework.serializers import ValidationError


class InvalidPK(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class CustomAPIException(ValidationError):
    status_code = 401
    default_code = 'error'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code

