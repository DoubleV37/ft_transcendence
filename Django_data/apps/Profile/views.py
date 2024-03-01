from django.http import JsonResponse
from django.shortcuts import render
from Auth.models import User

def profile(request):
    return render(request, "Profile/Profile.html")

def profilext(request):
    return render(request, "Profile/ForeignProfile.html")

def settings(request):
    return render(request, "Profile/Settings.html")

def get_profil_infos(request, user_id):
    if request.method != 'GET':
        return JsonResponse({'success': False})
    try:
        user = User.objects.get(id=user_id)
        status = user.status
        username = user.username
        avatar = user.avatar.url
        return JsonResponse({'success': True,
                             'status': status,
                             'username': username,
                             'avatar': avatar})

    except User.objects.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Wrong ID'})

def get_one_info(request, user_id, info_id):
    if request.method != 'GET':
        return JsonResponse({'success': False})
    try:
        user = User.objects.get(id=user_id)
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
