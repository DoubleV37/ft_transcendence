from django.views.generic import TemplateView
from apps.Auth.models import User
from django.shortcuts import render

import logging
logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = "Home/home.html"


class FooterView(TemplateView):
	template_name = "Home/footer.html"


def header(request):
    _user = request.user
    if _user.is_authenticated is True:
        _username = _user.username
        _avatar = _user.avatar.url
        if _user.in_game is True:
            _status = 'in game'
        elif _user.status is True:
            _status = 'online'
        else:
            _status = 'offline'
        _id = _user.id

        return render(
            request, 'Home/header.html', {'profil_picture': _avatar,
            'username': _username, 'status': _status,
            'id': _id}
        )
    return render(request, "Home/header.html")


def footer(request):
	return FooterView.as_view()(request)


def home(request):
	return HomeView.as_view()(request)
