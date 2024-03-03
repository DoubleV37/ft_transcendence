from django.shortcuts import render, redirect
from django.conf import settings

def profile(request):
    return render(request, "Profile/Profile.html")

def profilext(request):
    return render(request, "Profile/ForeignProfile.html")

def settings(request):
    return render(request, "Profile/Settings.html")

def avatar(request):
    return render(request, "Profile/Avatar.html")