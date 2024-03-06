import jwt
import datetime
from decouple import config
from asgiref.sync import iscoroutinefunction
from django.utils.decorators import sync_and_async_middleware

import logging

logger = logging.getLogger(__name__)

def create_jwt(_user, _type="access"):
    payload = {'id': _user.id,
               'username': _user.username,
               'email': _user.email}
    secret_key = config('DJANGO_SECRET_KEY')
    algorithm = config('HASH')
    if _type == "access":
        time_now = datetime.datetime.utcnow()
        payload['exp'] = time_now + datetime.timedelta(minutes=15)
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

class UserPermission:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)

        logger.info(request.META.get('HTTP_AUTHORIZATION'))

        return response
