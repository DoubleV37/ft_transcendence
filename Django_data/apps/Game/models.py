from django.db import models
from django.conf import settings


class MatchmakingUser(models.Model):
    channel_name = models.CharField(max_length=255, unique=True)
    user = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.channel_name


class Games(models.Model):
    idGame = models.CharField(max_length=255, unique=True)
    nb_users = models.IntegerField(default=0)
    running = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(default=0)
    pwr_up = models.BooleanField(default=False)
    nb_rounds = models.IntegerField(default=0)
    in_tournament = models.BooleanField(default=False)
    bounce = models.IntegerField(default=0)
    max_exchange = models.IntegerField(default=0)

    def __str__(self):
        return self.idGame


class UserGame(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    max_speed = models.FloatField(default=0)
    winner = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + " " + self.game.idGame
