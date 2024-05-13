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
        win_rate = round(_user.toGS.win_rate, 2)
        nb_games = _user.toGS.nb_games
        nb_tournament = _user.toGS.tournament_games

        return render(
            request, 'Home/header.html', {'profil_picture': _avatar,
            'username': _username, 'status': _status,
            'id': _id, 'win_rate': win_rate, 'nb_games': nb_games,
            'tournament_games': nb_tournament})
    return render(request, "Home/header.html")

def error404(request):
    return render(request, 'Errors/404.html')

def footer(request):
	return FooterView.as_view()(request)


def home(request):
	return HomeView.as_view()(request)
