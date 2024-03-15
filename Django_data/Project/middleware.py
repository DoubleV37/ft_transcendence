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
        home_path = ('/', '/header', '/footer')
        auth_path = ('/auth/signin/', '/auth/signup/', '/auth/jwt/refresh/',
                     '/2fa/confirm/')
        if request.path in home_path:  # look if path is ok for all type of user
            response = None
        elif request.path in auth_path:  # look if user is already logged or not
            response = self.auth_handler(request)
        else:
            response = self.logged_handler(request)
        return response


    def auth_handler(self, request):
        _user = request.user

        if _user.is_anonymous is False and request.path != '/auth/jwt/refresh/':
            return home(request)
        return None


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
            #self.log_error(encoded_token, "iss")
            logger.error(encoded_token)
            return HttpResponse("Bad Issuer", status=498)
        except jwt.ExpiredSignatureError:
            logger.error(encoded_token)
            #self.log_error(encoded_token, 'exp')
            return HttpResponse("Expired", status=498)
        except jwt.exceptions.InvalidTokenError:
            logger.error(encoded_token)
            signout(request)
            #self.log_error(encoded_token)
            return HttpResponse("Bad Token", status=498)


    def log_error(self, encoded_token, key=None):
        token_error = jwt.decode(encoded_token, config('DJANGO_SECRET_KEY'),
                                 algorithm=config('HASH'),
                                 options={"verify_signature": False})
        if key is None:
            logger.info("Invalid Token - %s", token_error)
        else:
            logger.info("Invalid Token - %s - %s", key, token_error.get(key))
