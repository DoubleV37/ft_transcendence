import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required

from .forms import (
        CustomUserCreationForm, SignInForm, InfoName, InfoMail, InfoPsswd, InfoAvatar,
        AllInfo, My_Psswd, My_Avatar, My_Name, My_Mail
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
            logger.debug(avatar_form.cleaned_data['avatar'])
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
                'errors': 'BAAAAAAAADDDDD'
            })
            if 'avatar' in request.FILES:
                avatar_form = InfoAvatar(request.POST, request.FILES, instance=user)
                if  avatar_form.is_valid():
                    logger.debug("forth requset if")
                    avatar = avatar_form.save(commit=False)
                    logger.debug(avatar_form.cleaned_data['avatar'])
                    user.avatar = avatar.avatar
                    logger.debug("0")
                    user.username = request.user.username
                    user.save()
                    logger.debug("1")
                    response = JsonResponse({
                        'success': True,
                        'key': 'Photo',
                    })
            if  form.is_valid():
                logger.debug("Second requset if")
                form.save()
                response = JsonResponse({
                    'success': True,
                    'key': 'User...',
                })
            logger.debug(form.errors)
            return response
        logger.debug("Displaying html")
        return render(request, 'AllInfo.html', context=context)
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        logger.debug("Exception")
        return HttpResponse("Exception", status=400)


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
            'errors': 'BAAAAAAAADDDDD'
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
                logger.debug("avatar")
                save = avatar.save(commit=False)
                user.username = request.user.username
                user.avatar = save.avatar
                user.save()
                response = JsonResponse({
                    'success': True,
                    'key': 'avatar'
                })
            else:
                logger.debug("else avatar")
                errors = mail.errors
                response = JsonResponse({'success': False, 'errors': errors})
            if name.is_valid():
                logger.debug("name")
                name.save()
                response = JsonResponse({
                    'success': True,
                    'key': 'name'
                })
            else:
                logger.debug("else name")
                errors = mail.errors
                response = JsonResponse({'success': False, 'errors': errors})
            if mail.is_valid():
                logger.debug("mail")
                mail.save()
                response = JsonResponse({
                    'success': True,
                    'key': 'mail'
                })
            else:
                logger.debug("else mail")
                errors = mail.errors
                response = JsonResponse({'success': False, 'errors': errors})


            if pswd.is_valid():
                logger.debug("pswd")
                pswd.save()
                response = JsonResponse({
                    'success': True,
                    'key': 'pswd'
                })
            else:
                logger.debug("else pswd")
                errors = mail.errors
                response = JsonResponse({'success': False, 'errors': errors})

            return response
        return render(request, 'My_Settings.html', context=context)
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        logger.debug("Exception")
        return HttpResponse("Exception", status=400)


