import json
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from Project.middleware import create_jwt
from .forms import (
    CustomUserCreationForm, SignInForm, My_Psswd,
    My_Avatar, My_Name, My_Mail, My_Tournamentname
)
from .models import User
from django.http import HttpResponse


logger = logging.getLogger(__name__)

# ___________________________________________________________________________ #
# _ SINGNUP _________________________________________________________________ #

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # user = form.save()
            # login(request, user)
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': form.errors})
    form = CustomUserCreationForm()
    return render(request, 'Auth/SignUp.html', {'form': form})

# ___________________________________________________________________________ #
# _ SINGNIN _________________________________________________________________ #


def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                jwt_token = create_jwt(user)
                response = HttpResponse()
                response.set_cookie(key='jwt_token',
                                    value=str(jwt_token),
                                    httponly=True,
                                    secure=True,
                                    samesite='Lax')
            else:
                response = HttpResponse('incorrect username or password',
                                        status=401)
        else:
            response = HttpResponse('Invalid Form', status=401)
        return response

    form = SignInForm()
    return render(request, 'Auth/SignIn.html', {'form': form})

# ___________________________________________________________________________ #
# _ SINGNOUT ________________________________________________________________ #


def signout(request):
    user = request.user
    user.refresh_token = None
    user.save()
    logout(request)
    response = HttpResponse()
    response.delete_cookie('access_token')
    return response


# ___________________________________________________________________________ #
# _ MY SETTINGS _____________________________________________________________ #

def validator_fct(form, button: str, request, response: dict()) -> dict():
    if response.__len__ == 0:
        return response
    if button in request.POST:
        if form.is_valid():
            form.save()
            response = {'success': True}
        else:
            response = {
                'success': False,
                'logs': f'{button} Error'
            }
    return response


def my_settings(request):
    try:
        _user = User.objects.get(username=request.user.username)

        name = My_Name(instance=_user)
        mail = My_Mail(instance=_user)
        pswd = My_Psswd(instance=_user)
        avatar = My_Avatar(instance=_user)
        t_name = My_Tournamentname(instance=_user)

        response: dict() = {}
        context: dict() = {
            '_user': _user, 'name': name, 'mail': mail,
            'avatar': avatar, 'pswd': pswd, 't_name': t_name
        }

        if request.method == 'POST':
            name = My_Name(request.POST, instance=_user)
            mail = My_Mail(request.POST, instance=_user)
            pswd = My_Psswd(request.POST, instance=_user)
            avatar = My_Avatar(request.POST, request.FILES, instance=_user)
            t_name = My_Tournamentname(request.POST, instance=_user)

            if 'avatar_button' in request.POST:
                if avatar.is_valid():
                    save = avatar.save(commit=False)
                    _user._username = request._user._username
                    _user.avatar = save.avatar
                    _user.save()
                    response = {'success': True}
                else:
                    response = {
                        'success': False,
                        'logs': 'Avatar Error'
                    }

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
