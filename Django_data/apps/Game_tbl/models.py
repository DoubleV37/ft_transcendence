from django.db import models
from django.conf import settings

class PlayerInfo(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='toPI',
        on_delete=models.CASCADE, primary_key=True,
    )

    victory = models.BooleanField()
    score = models.IntegerField(default=0)
    rebounds = models.IntegerField(default=0)
    max_ball_speed = models.IntegerField(default=0)
    collected_bonus = models.IntegerField(default=0)



class GameHistory(models.Model):

    player1 = models.OneToOneField(
        PlayerInfo, related_name='p1toGH',
        on_delete=models.CASCADE,
    )
    player2 = models.OneToOneField(
        PlayerInfo, related_name='p2toGH',
        on_delete=models.CASCADE,
    )

    date = models.DateTimeField(auto_now_add=True)
    max_exchange = models.IntegerField(default=0)
