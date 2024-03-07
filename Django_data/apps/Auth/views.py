import json
import logging
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate, logout

from Project.middleware import create_jwt

from .forms import (
        CustomUserCreationForm, SignInForm, My_Psswd,
        My_Avatar, My_Name, My_Mail, My_Tournamentname
    )
from .models import User

logger = logging.getLogger(__name__)


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


def signout(request):
    user = request.user
    user.refresh_token = None
    user.save()
    logout(request)
    response = HttpResponse()
    response.delete_cookie('access_token')
    return response


def my_settings(request):
    try:
        user = User.objects.get(username=request.user.username)

        rtrn = 0
        name = My_Name(instance=user)
        mail = My_Mail(instance=user)
        pswd = My_Psswd(instance=user)
        avatar = My_Avatar(instance=user)
        t_name = My_Tournamentname(instance=user)


        response = JsonResponse({
            'success': False,
            'errors': 'unexpected'
        })

        context = {
            'user': user, 'name': name, 'mail': mail,
            'avatar': avatar, 'pswd': pswd, 't_name': t_name
        }

        if request.method == 'POST':
            name = My_Name(request.POST, instance=user)
            mail = My_Mail(request.POST, instance=user)
            pswd = My_Psswd(request.POST, instance=user)
            avatar = My_Avatar(request.POST, request.FILES, instance=user)
            t_name = My_Tournamentname(request.POST, instance=user)
            logger.debug(request.POST)

            if avatar.is_valid():
                save = avatar.save(commit=False)
                user.username = request.user.username
                user.avatar = save.avatar
                user.save()
            elif pswd.is_valid():
                pswd.save()
            else:
                pass

            if t_name.is_valid():
                t_name.save()
            elif 't_name_button' in request.POST:
                errors = t_name.errors
                logger.debug("111111")
                logger.error(f"Exception occurred: {errors}")
                rtrn = 3
            else:
                pass

            if name.is_valid():
                name.save()
            elif 'name_button' in request.POST:
                errors = name.errors
                logger.debug("222222")
                logger.error(f"Exception occurred: {errors}")
                rtrn = 1
            else:
                pass

            if mail.is_valid():
                mail.save()
            elif 'mail_button' in request.POST:
                rtrn = 2
            else:
                pass

            match rtrn:
                case 1:
                    return JsonResponse({ 'success': False,
                        'errors': 'username already taken'
                    })
                case 2:
                    return JsonResponse({ 'success': False,
                        'errors': 'email already taken'
                    })
                case 3:
                    return JsonResponse({ 'success': False,
                        'errors': 'tournament name already taken'
                    })
                case _:
                    return JsonResponse({'success': True})

        return render(request, 'My_Settings1.html', context=context)

    except Exception as e:
        logger.debug("Exception")
        logger.error(f"Exception occurred: {e}")
        return HttpResponse("Exception", status=400)


