from django.shortcuts import render, redirect
from apps.Auth.models import User
from django.http import JsonResponse

def gamePage(request, _id=None, *args, **kwargs ):
    try:
        if _id is None:
            _user = request.user
            _type = 'himself'
        else:
            _user = User.objects.get(idUser=_id)
            _type = 'foreign'
        _username = _user.username
        _avatar = _user.avatar.url
        return render(request, "Game/gamePage.html", 
                    {
                    'profil_picture': _avatar,
                    'username': _username,
                    })
    except User.objects.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Wrong ID'})

def gameParameters(request):
    return render(request, "Game/Parameters.html")

def modes(request):
    return render(request, "Game/Modes.html")

def tournament(request):
    return render(request, "Game/Tournament.html")