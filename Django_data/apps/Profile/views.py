from django.http import JsonResponse
from django.shortcuts import render
from apps.Auth.models import User


import logging
logger = logging.getLogger(__name__)


def settings(request):
    return render(request, "Profile/Settings.html")


def profile_infos(request, _id=None):
    try:
        if _id is None:
            _user = request.user
            _type = 'himself'
        else:
            _user = User.objects.get(idUser=_id)
            _type = 'foreign'
        _status = 'online' if _user.status is True else 'offline'
        _username = _user.username
        _avatar = _user.avatar.url
        return render(request, 'Profile/Profile.html',
                      {'profile': _type,
                       'profil_picture': _avatar,
                       'username': _username,
                       'status': _status})
    except User.objects.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Wrong ID'})


def avatar(request):
    return render(request, "Profile/Avatar.html")
