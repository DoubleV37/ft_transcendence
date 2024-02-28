import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required

from .forms import (
        CustomUserCreationForm, SignInForm, InfoName, InfoMail, InfoPsswd, InfoAvatar,
        AllInfo
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

def edit_avatar(request):
    user = User.objects.get(username=request.user.username)
    logger.debug("edit_avatar")
    if request.method == 'POST' and 'avatar' in request.FILES:
        logger.debug("first condition in")
        avatar_form = InfoAvatar(request.POST, request.FILES, instance=user)
        if avatar_form.is_valid():
            logger.debug("is_valid=True")
            avatar = avatar_form.save(commit=False)
            user.avatar = avatar.avatar
            user.save()
            response = JsonResponse({'success': True})
            return response
        else:
            logger.debug("is_valid=False")
            response = JsonResponse(
                {'success': False,
                'errors': 'Invalid form'}
            )
            return response
    else:
        avatar_form = InfoAvatar(instance=user)
        return render(request, 'edit_avatar.html', {'avatar_form': avatar_form})
    logger.debug("Che ne pas comprende")
    return HttpResponse("Exception", status=400)

def edit_name(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        if 'username' in request.POST:
            name = InfoName(request.POST, instance=user)
            if name.is_valid():
                name.save()
                response = JsonResponse({'success': True})
                return response
        else:
            response = JsonResponse(
                {'success': False,
                 'errors': 'Invalid form'}
            )
            return response
    else:
        name = InfoName(instance=user)
        return render(request, 'edit_name.html', {'name': name})

def edit_psswd(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        if 'password1' in request.POST:
            psswd = InfoPsswd(request.POST, instance=user)
            if psswd.is_valid():
                psswd.save()
                response = JsonResponse({'success': True})
                return response
        else:
            response = JsonResponse(
                {'success': False,
                 'errors': 'Invalid form'}
            )
            return response
    else:
        psswd = InfoPsswd(instance=user)
        return render(request, 'edit_psswd.html', {'psswd': psswd})

def edit_mail(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        if 'email' in request.POST:
            mail = InfoMail(request.POST, instance=user)
            if mail.is_valid():
                mail.save()
                response = JsonResponse({'success': True})
                return response
        else:
            response = JsonResponse(
                {'success': False,
                 'errors': 'Invalid form'}
            )
            return response
    else:
        mail = InfoMail(instance=user)
        return render(request, 'edit_mail.html', {'mail': mail})

# @login_required
def info(request):
    try:
        user = User.objects.get(username=request.user.username)
        return render(request, 'Info.html', {'user': user})
    except:
        return HttpResponse("Exception", status=400)

def allinfo(request):
    try:
        user = User.objects.get(username=request.user.username)
        form = AllInfo(instance=user)
        avatar_form = InfoAvatar(instance=user)
        context={
            'user': user,
            'form': form,
            'avatar_form': avatar_form,
        }
        if request.method == 'POST':
            logger.debug("First requset if")
            form = AllInfo(request.POST, instance=user)
            response = JsonResponse({
                'success': False,
                'errors': 'Initial',
            })
            if  form.is_valid():
                logger.debug("Second requset if")
                form.save()
                response = JsonResponse({'success': True})
            else:
                logger.debug("Second requset else")
                response = JsonResponse({
                    'success': False,
                    'errors': 'FORM'
                })
            if 'avatar' in request.POST :
                logger.debug("third requset if")
                avatar_form = InfoAvatar(request.POST, request.FILES,instance=user)
                if  avatar_form.is_valid():
                    avatar = avatar_form.save(commit=False)
                    logger.debug(avatar_form.cleaned_data['avatar'])
                    user.avatar = avatar.avatar
                    user.save()
                    response = JsonResponse({'success': True})
            else:
                logger.debug("third requset else")
                response = JsonResponse({
                    'success': False,
                    'errors': 'Photo'
                })
            return response
        logger.debug("Displaying html")
        return render(request, 'AllInfo.html', context=context)
    except:
        logger.debug("Exception")
        return HttpResponse("Exception", status=400)


def signout(request):
    if request.method == 'POST':
        logout(request)
    return JsonResponse({'success': True})
