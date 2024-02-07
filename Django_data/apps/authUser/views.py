from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, SignInForm


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'cygne_up.html', context)


def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                response = JsonResponse({'success': True})
            else:
                form.add_error(None, 'Invalid username or password')
                response = JsonResponse({'success': False,
                                         'errors': form.errors})
        else:
            response = JsonResponse({'success': False, 'errors': form.errors})
        return response

    form = SignInForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)
