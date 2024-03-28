from django.shortcuts import render, redirect

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
