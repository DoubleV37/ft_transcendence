from django.db import models
from django.conf import settings

import logging
logger = logging.getLogger(__name__)


class GlobalStats(models.Model):

	user = models.OneToOneField(
		settings.AUTH_USER_MODEL, related_name='toGS',
		on_delete=models.CASCADE, primary_key=True,
	)

	win_rate = models.FloatField(default=0.0)
	nb_games = models.IntegerField(default=0)
	regular_games = models.IntegerField(default=0)
	tournament_games = models.IntegerField(default=0)
	victory = models.IntegerField(default=0)
	defeat = models.IntegerField(default=0)
	victory_ia = models.IntegerField(default=0)
	victory_player = models.IntegerField(default=0)
