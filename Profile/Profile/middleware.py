import logging
import jwt
from decouple import config
from django.http import HttpResponse
from apps.Home.views import home
from apps.Auth.views import signin, signout

logger = logging.getLogger(__name__)


class UserPermission:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)
        return response


    def process_view(self, request, view_func, view_args, view_kwargs):
        authorised_path = ('/',
                           '/header',
                           '/footer',
                           '/auth/signin/',
                           '/auth/signup/',
                           '/auth/jwt/refresh/',
                           '/2fa/confirm/')
        logger.info(f"path -> {request.path}")
        logger.info(f"request =>\n {request}")
        if request.path in authorised_path:
            response = None
        else:
            response = self.logged_handler(request)
        return response


    def logged_handler(self, request):
        try:
            _user = request.user
            if _user.is_anonymous is True:
                return signin(request)

            encoded_token = request.COOKIES.get('jwt_token')
            if encoded_token is None:
                signout(request)
                return HttpResponse("Unauthorized login Session", status=499)
            _options = {'verify_exp': True, 'verify_iss': True}
            jwt.decode(encoded_token, config('DJANGO_SECRET_KEY'),
                       algorithms=config('HASH'), issuer=config('NAME'),
                       options=_options)
            return None
        except jwt.InvalidIssuerError:
            signout(request)
            logger.error(f" Invalid Issuer : {encoded_token}")
            return HttpResponse("Bad Issuer", status=498)
        except jwt.ExpiredSignatureError:
            logger.error(f"expired token {encoded_token}")
            return HttpResponse("Expired", status=498)
        except jwt.exceptions.InvalidTokenError:
            logger.error(f"Invalid token : {encoded_token}")
            signout(request)
            return HttpResponse("Bad Token", status=498)
