import logging, datetime, jwt, json
from decouple import config
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate, logout

from .forms import (
    CustomUserCreationForm, SignInForm, My_Psswd,
    My_Avatar, My_Name, My_Mail, My_Tournamentname,
    DeleteAvatar
)
from .models import User
from apps.Twofa.models import UserTwoFA
from apps.Twofa.forms import My_2fa

logger = logging.getLogger(__name__)

# ___________________________________________________________________________ #
# _ SINGNUP _________________________________________________________________ #

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': form.errors})
    form = CustomUserCreationForm()
    return render(request, 'Auth/SignUp.html', {'form': form})

# ___________________________________________________________________________ #
# _ SINGNIN _________________________________________________________________ #

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        logger.info(f"request => \n{request}")
        data_response: dict() = {}

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:

                if user.to2fa.enable:
                    response = JsonResponse({'success': True, 'Twofa': True})
                else:
                    data_response = {'success': True, '2fa': False}
                    login(request, user)
                    jwt_token = create_jwt(user)
                    response = JsonResponse(data_response)
                    response.set_cookie(
                        key='jwt_token', value=str(jwt_token),
                        httponly=True, secure=True,
                        samesite='Lax')
                return response
            else:
                response = JsonResponse({'success': False,
                                        'error':
                                            'incorrect username or password'})
        else:
            response = JsonResponse({'success': False,
                                     'error': 'Wrong form'})
        return response
    form = SignInForm()
    return render(request, 'Auth/SignIn.html', {'form': form})

# ___________________________________________________________________________ #
# _ SINGNOUT ________________________________________________________________ #

def signout(request):
    logout(request)
    response = HttpResponse(status=200)
    response.delete_cookie('jwt_token')
    return response


# ___________________________________________________________________________ #
# _ MY SETTINGS _____________________________________________________________ #

def validator_fct(form, button: str, request, response: dict()) -> dict():
    if button in request.POST:
        if form.is_valid():
            form.save()
            response = {'success': True}
        else:
            response = {'success': False, 'logs': f'{button} Error'}
    return response


def my_settings(request):

    try:
        my_user = User.objects.get(username=request.user.username)

        name = My_Name(instance=my_user)
        mail = My_Mail(instance=my_user)
        pswd = My_Psswd(instance=my_user)
        avatar = My_Avatar(instance=my_user)
        t_name = My_Tournamentname(instance=my_user)
        delete_avatar = DeleteAvatar()

        response: dict() = {}
        context: dict() = {
            'my_user': my_user, 'name': name, 'mail': mail,
            'avatar': avatar, 'pswd': pswd, 't_name': t_name,
            'delete_avatar': delete_avatar,
        }

        if request.method == 'POST':
            name = My_Name(request.POST, instance=my_user)
            mail = My_Mail(request.POST, instance=my_user)
            pswd = My_Psswd(request.POST, instance=my_user)
            avatar = My_Avatar(request.POST, request.FILES, instance=my_user)
            t_name = My_Tournamentname(request.POST, instance=my_user)
            delete_avatar = DeleteAvatar(request.POST)

            if 'avatar_button' in request.POST:
                if avatar.is_valid():
                    save = avatar.save(commit=False)
                    my_user.username = request.user.username
                    my_user.avatar = save.avatar
                    my_user.save()
                    response = {'success': True}
                else:
                    response = {'success': False, 'logs': 'Avatar Error'}

            if 'avatar_delete' in request.POST:
                if delete_avatar.is_valid():
                    if my_user.avatar.url.find("ForbiddenDeletion/") == -1:
                        my_user.avatar.delete()
                        my_user.avatar = my_user.backup_avatar
                        my_user.save()
                        response = {'success': True}
                    else:
                        response = {'success': False, 'logs': 'default.png'}
                else:
                    response = {'success': False, 'logs': 'Avatar not deleted'}

            response = validator_fct(name, 'name_button', request, response)
            response = validator_fct(
                t_name, 't_name_button', request, response)
            response = validator_fct(pswd, 'pswd_button', request, response)
            response = validator_fct(mail, 'mail_button', request, response)

            return JsonResponse(response)
        return render(request, 'My_Settings1.html', context=context)

    except Exception as e:
        logger.debug("Exception")
        logger.error(f"Exception occurred: {e}")
        return HttpResponse("Exception", status=400)


# ___________________________________________________________________________ #
# _  JWT ____________________________________________________________________ #


def refresh_jwt(request):
    logger.info(request.method)
    if request.method == 'GET':
        logger.info('aled 1')
        user = request.user
        logger.info('aled 2')
        logger.info(user.refresh_token)
        if user.refresh_token is None:
            logger.info('aled 3')
            return HttpResponse("Bad Token", status=498)
        logger.info('aled 4')
        jwt_token = create_jwt(user)
        response = HttpResponse()
        response.set_cookie(key='jwt_token',
                            value=str(jwt_token),
                            httponly=True,
                            secure=True,
                            samesite='Lax')
        return response
    return HttpResponse("Exception", status=400)


def create_jwt(_user, _type="access"):
    payload = {'id': _user.id,
               'username': _user.username,
               'email': _user.email}
    secret_key = config('DJANGO_SECRET_KEY')
    algorithm = config('HASH')
    if _type == "access":
        time_now = datetime.datetime.utcnow()
        payload = {"exp": time_now + datetime.timedelta(hours=1),
                   "iss": config('NAME')}
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token
