from django.http import JsonResponse
from django.shortcuts import render
from apps.Auth.models import User
import logging


logger = logging.getLogger(__name__)

def profile(request):
    return render(request, "Profile/Profile.html")


def profilext(request):
    return render(request, "Profile/ForeignProfile.html")


def settings(request):
    return render(request, "Profile/Settings.html")


def get_profil_infos(request, user_id):
    logger.debug(f"aled --- {request}--------{user_id}")
    if request.method != 'GET':
        return JsonResponse({'success': False})
    try:
        user = User.objects.get(idUser=user_id)
        status = user.status
        username = user.username
        avatar = user.avatar.url
        profile_type = ''
        if request.user.idUser == user.idUser:
            profile_type = 'himself'
        else:
            profile_type = 'foreign'
        return render(request, 'Profile/Profile.html',
                      {'profile': profile_type,
                       'profil_picture': avatar,
                       'username': username,
                       'status': status})
    except User.objects.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Wrong ID'})


def get_one_info(request, user_id, info_id):
    logger.info("I\'M HERE ???")
    if request.method != 'GET':
        return JsonResponse({'success': False})
    try:
        user = User.objects.get(idUser=user_id)
        match info_id:
            case 0:
                info = 'status'
                data = user.status
            case 1:
                info = 'username'
                data = user.username
            case 2:
                info = 'avatar'
                data = user.avatar.url
            case _:
                raise NameError('Info doesn\'t exist !')
        return JsonResponse({'success': True,
                             info: data})
    except User.objects.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Wrong ID'})
    except NameError as e:
        return JsonResponse({'success': False, 'error': str(e.args[0])})


def avatar(request):
    return render(request, "Profile/Avatar.html")
