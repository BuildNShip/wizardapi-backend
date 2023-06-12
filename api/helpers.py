import string
import random

from apps.api_data.models import UserToken


def generate_unique_api_token():
    token = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(10))
    unique_confirm = UserToken.objects.filter(deleted_at__isnull=True, status=UserToken.ACTIVE,
                                              api_token=token).first()
    while unique_confirm:
        token = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(10))
        if not UserToken.objects.filter(deleted_at__isnull=True, status=UserToken.ACTIVE,
                                        api_token=token).first():
            break
    return token
