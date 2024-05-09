from django.shortcuts import render, redirect
from .models import Games, UserGame
from apps.Auth.models import User
from django.http import JsonResponse


def gamePage(request, _id=None, *args, **kwargs):
    try:
        if _id is None:
            _user = request.user
            _type = "himself"
        else:
            _user = User.objects.get(idUser=_id)
            _type = "foreign"
        _username = _user.username
        _avatar = _user.avatar.url
        return render(
            request,
            "Game/gamePage.html",
            {
                "profil_picture": _avatar,
                "username": _username,
                "background": _user.skin_background,
            },
        )
    except User.objects.DoesNotExist:
        return JsonResponse({"success": False, "error": "Wrong ID"})


def multiGamePage(request, room_name):
    if not request.user.is_authenticated:
        return redirect("/")
    context = {
        "room_name": room_name,
        "background": request.user.skin_background,
        "username": request.user.username,
        "profil_picture": request.user.avatar.url,
    }
    return render(request, "Game/gamePage.html", context)


def matchmakingPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("/")
    context = {}
    return render(request, "Game/matchmaking.html", context)


def gameParameters(request):
    return render(request, "Game/Parameters.html")


def modes(request):
    return render(request, "Game/Modes.html")


def tournament(request):
    return render(request, "Game/Tournament.html")


def gameParameters(request):
    return render(request, "Game/Parameters.html")


def modes(request):
    return render(request, "Game/Modes.html")


def tournament(request):
    return render(request, "Game/Tournament.html")
