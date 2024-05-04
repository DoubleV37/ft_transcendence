from .models import GlobalStats
from apps.Auth.models import User
from apps.Game.models import Games, UserGame


import logging
logger = logging.getLogger(__name__)


def populate(key: User) -> dict:
    context = dict()
    data = GlobalStats.objects.get(user=key)
    context['win_rate'] = data.win_rate
    context['nb_games'] = data.nb_games
    context['regular_games'] = data.regular_games
    context['tournament_games'] = data.tournament_games
    context['victory'] = data.victory
    context['defeat'] = data.defeat
    context['tournaments_winned'] = data.tournaments_winned
    return context
