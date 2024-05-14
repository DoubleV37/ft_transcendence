from .models import GlobalStats
from apps.Auth.models import User
from apps.Game.models import Games, UserGame


import logging
logger = logging.getLogger(__name__)


def populate(key: User) -> dict:
	context = dict()
	data = GlobalStats.objects.get_object_or_404(user=key)
	context['win_rate'] = round(data.win_rate, 2)
	context['nb_games'] = data.nb_games
	context['regular_games'] = data.regular_games
	context['tournament_games'] = data.tournament_games
	context['victory'] = data.victory
	context['defeat'] = data.defeat
	context['victory_ia'] = data.victory_ia
	context['victory_player'] = data.victory_player
	context['user'] = key.username
	return context
