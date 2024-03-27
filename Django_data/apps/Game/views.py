from django.shortcuts import render, redirect

def gamePage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("/")
    context = {}
    return render(request, "Game/gamePage.html", context)

def gameParameters(request):
    return render(request, "Game/Parameters.html")

def modes(request):
    return render(request, "Game/Modes.html")

def tournament(request):
    return render(request, "Game/Tournament.html")