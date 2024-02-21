from django.shortcuts import render, redirect
from django.conf import settings

def profile(request):
    return render(request, "Profile/Profile.html")