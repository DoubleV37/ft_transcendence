from django.shortcuts import render, redirect
from .models import Games, UserGame

def gamePage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("/")
    context = {}
    return render(request, "Game/gamePage.html", context)

def multiGamePage(request, room_name):
	if not request.user.is_authenticated:
		return redirect("/")
	context = {"room_name": room_name}

	return render(request, "Game/multiGamePage.html", context)

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
