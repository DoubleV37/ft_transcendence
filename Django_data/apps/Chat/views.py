from django.shortcuts import render, redirect

def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("/")
    context = {}
    return render(request, "Chat/chatPage.html", context)
