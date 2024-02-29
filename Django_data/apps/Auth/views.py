import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required

from .forms import (
        CustomUserCreationForm, SignInForm, My_Psswd, My_Avatar, My_Name, My_Mail
    )
from . import forms

from .models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


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
    else:
        form = CustomUserCreationForm()
    return render(request, 'Auth/SignUp.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = SignInForm(data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                response = JsonResponse({'success': True})
            else:
                response = JsonResponse({'success': False,
                                         'errors':
                                         'Invalid username or password'})
        else:
            response = JsonResponse({'success': False,
                                     'errors': 'Invalid form'})
        return response

    form = SignInForm()
    return render(request, 'Auth/SignIn.html', {'form': form})

def signout(request):
    if request.method == 'POST':
        logout(request)
    return JsonResponse({'success': True})


def my_settings(request):
    try:
        user = User.objects.get(username=request.user.username)
        name = My_Name(instance=user)
        mail = My_Mail(instance=user)
        pswd = My_Psswd(instance=user)
        avatar = My_Avatar(instance=user)
        response = JsonResponse({
            'success': False,
            'errors': 'unexpected'
        })
        context = {
            'user': user,
            'name': name,
            'mail': mail,
            'avatar': avatar,
            'pswd': pswd,
        }
        if request.method == 'POST':
            name = My_Name(request.POST, instance=user)
            mail = My_Mail(request.POST, instance=user)
            pswd = My_Psswd(request.POST, instance=user)
            avatar = My_Avatar(request.POST, request.FILES, instance=user)

            if avatar.is_valid():
                save = avatar.save(commit=False)
                user.username = request.user.username
                user.avatar = save.avatar
                user.save()
                response = JsonResponse({'success': True})
            else:
                pass

            if name.is_valid():
                name.save()
                response = JsonResponse({'success': True})
            else:
                response = JsonResponse({
                    'success': False,
                    'errors': 'bad name'
                })

            if mail.is_valid():
                mail.save()
                response = JsonResponse({'success': True})
            else:
                response = JsonResponse({
                    'success': False,
                    'errors': 'bad mail'
                })

            if pswd.is_valid():
                pswd.save()
                response = JsonResponse({'success': True})
            else:
                pass

            return response

        return render(request, 'My_Settings.html', context=context)

    except Exception as e:
        logger.debug("Exception")
        logger.error(f"Exception occurred: {e}")
        return HttpResponse("Exception", status=400)


