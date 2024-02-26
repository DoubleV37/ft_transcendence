import json
import logging
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required

from .forms import CustomUserCreationForm, SignInForm, InfoName, InfoMail, InfoPsswd
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

        # if 'edit_blog' in request.POST:
        #     edit_form = forms.BlogForm(request.POST, instance=blog)
        #     if edit_form.is_valid():
        #         edit_form.save()
        #         return redirect('home')
        # if 'delete_blog' in request.POST:
        #     delete_form = forms.DeleteBlogForm(request.POST)
        #     if delete_form.is_valid():
        #         blog.delete()
        #         return redirect('home')

# @login_required
def edit_name(request):
    user = User.objects.get(username=request.user.username)
    # logger.debug(request)
    logger.debug("test 1")
    if request.method == 'POST':
        if 'username' in request.POST:
            # data = json.loads(request.body)
            logger.debug("test 2")
            name = InfoName(request.POST, instance=user)
            if name.is_valid():
                name.save()
                return redirect(LOGIN_REDIRECT_URL)
        else:
            return HttpResponse("User does not exist or is not authenticated.", status=404)
    else:
        logger.debug("test 3")
        name = InfoName(instance=user)
        return render(request, 'edit_name.html', {'name': name})


# @login_required
# @permission_required('Auth/SignUp.html', raise_exception=True)
def info(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'Info.html', {'user': user})
    # name = InfoName(instance=user)
    # mail = InfoMail(instance=user)
    # psswd = InfoPsswd(instance=user)
    # context={
    #     'name': name,
        # 'mail': mail,
        # 'psswd': psswd,
    # }
    # if request.method == 'POST':
    #
    #     if 'name_update' in request.POST:
    #         name = InfoName(request.POST, instance=user)
    #         if name.is_valid():
    #             name = form.cleaned_data['name']
    #             name.save()
    #             response = JsonResponse({'success': True})
    #             return redirect('edit_name')
            # else:
            #     response = JsonResponse({'success': False,
            #                             'errors':
            #                             'Invalid username or password'})

        # if 'password_update' in request.POST:
        #     psswd = InfoPsswd(request.POST, instance=user)
        #     if psswd.is_valid():
        #         print("name ICI 03") # TODO DEBUG
        #         response = JsonResponse({'success': True})
        #         return redirect('home')
            # else:
            #     response = JsonResponse({'success': False,
            #                             'errors':
            #                             'Invalid username or password'})

        # if 'email_update' in request.POST:
        #     print("name ICI 04") # TODO DEBUG
        #     mail = InfoMail(request.POST, instance=user)
        #     # email = form.cleaned_data['email']
        #     if mail.is_valid():
        #         print("name ICI 05") # TODO DEBUG
        #         response = JsonResponse({'success': True})
        #         return redirect('home')
            # else:
            #     response = JsonResponse({'success': False,
            #                             'errors':
            #                             'Invalid Mail'})

        # else:
        #     response = JsonResponse({'success': False,
        #                                 'errors': 'Invalid form'})
        # return response

def signout(request):
    if request.method == 'POST':
        logout(request)
    return JsonResponse({'success': True})
