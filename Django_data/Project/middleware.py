import logging
import jwt
from decouple import config
from django.http import HttpResponse
from apps.Home.views import home
from apps.Auth.views import signin

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
        auth_path = ('/auth/signin/', '/auth/signup/')
        if request.path in home_path:  # look if path is ok for all type of user
            response = None
        elif request.path in auth_path:  # look if user is already logged or not
            response = self.auth_handler(request)
        else:
            response = self.logged_handler(request)
        return response


    def auth_handler(self, request):
        _user = request.user

        if _user.is_anonymous is False:
            return home(request)
        logger.debug("i\'m here motherfucker")
        return None


    def logged_handler(self, request):
        _user = request.user

        if _user.is_anonymous is True:
            if request.method == 'GET':
                return signin(request)
            # ah je sais pas encore pour les POST et autres
            return None
        try:
            encoded_token = request.COOKIES.get('jwt_token')
            if encoded_token is None:
                return HttpResponse("Unauthorized login Session", status=499)
            _options = {'verify_exp': True, 'verify_iss': True}
            jwt.decode(encoded_token, config('DJANGO_SECRET_KEY'),
                       algorithms=config('HASH'), issuer=config('NAME'),
                       options=_options)
            return None
        except jwt.InvalidIssuerError:
            token_error = jwt.decode(encoded_token, config('DJANGO_SECRET_KEY'),
                                     algorithm=config('HASH'),
                                     options={"verify_signature": False})
            logger.info("InvalidIssuer - %s", token_error.get('iss'))
            return HttpResponse("Invalid Token - Bad Issuer", status=498)
        except jwt.ExpiredSignatureError:
            token_error = jwt.decode(encoded_token, config('DJANGO_SECRET_KEY'),
                                     algorithm=config('HASH'),
                                     options={"verify_signature": False})
            logger.info("Token has expired - %s", token_error.get('exp'))
            return HttpResponse("Invalid Token - Expired", status=498)
        except jwt.exceptions.InvalidTokenError:
            token_error = jwt.decode(encoded_token, config('DJANGO_SECRET_KEY'),
                                     algorithm=config('HASH'),
                                     options={"verify_signature": False})
            logger.info("Bad Token - %s", token_error.str)
            return HttpResponse("Invalid Token - Bad Token", status=498)
