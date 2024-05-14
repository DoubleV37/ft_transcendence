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
  if request.method == "GET":
    # if "Load" not in request.headers:
    #   return redirect("/game/modes/")
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
  if request.method == "GET":
    if not request.user.is_authenticated:
        return redirect("/")
    context = {}
    return render(request, "Game/matchmaking.html", context)


def gameParameters(request):
  if request.method == "GET":
    return render(request, "Game/Parameters.html")


def modes(request):
  if request.method == "GET":
    return render(request, "Game/Modes.html")


def tournament(request):
    if request.method == "GET":
        context = {}
        context['username_tournament'] = request.user.tournament_name
    return render(request, "Game/Tournament.html", context)

def bracket(request):
    if request.method == "GET":
        return render(request, "Game/Bracket.html")
