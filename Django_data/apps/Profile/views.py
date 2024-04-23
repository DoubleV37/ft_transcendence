from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import render
from apps.Auth.models import User
import logging


logger = logging.getLogger(__name__)


def settings(request):
    return render(request, "Profile/Settings.html")


def profile_infos(request, _id=None):
    item = {}
    if _id is None:
        _user = request.user
        item['type'] = 'himself'
    else:
        _user = User.objects.get(id=_id)
        item['type'] = 'foreign'
        item['status'] = calculate_deltatime(_user)
    item['username'] = _user.username
    item['avatar'] = _user.avatar.url
    return render(request, 'Profile/Profile.html', item)


def avatar(request):
    return render(request, "Profile/Avatar.html")

def skin(request):
    if request.method == 'GET':
        return render(request, "Profile/Skins.html")

def calculate_deltatime(_user):
    if _user.in_game is True:
        return 'ingame'
    current_time = timezone.now()
    last_time_ping = _user.online_data
    delta_time = current_time - last_time_ping
    if delta_time > timedelta(seconds=3):
        return 'offline'
    return 'online'
