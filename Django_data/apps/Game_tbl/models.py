from django.db import models
from django.conf import settings

class Game(models.Model):

    me = models.ManyToManyField(settings.AUTH_USER_MODEL)

    enemy = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='toGame',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    ball_touched = models.IntegerField(default=0)
    victory = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    my_score = models.IntegerField(default=0)
    enemy_score = models.IntegerField(default=0)
    rebounds = models.IntegerField(default=0)
    my_max_ball_speed = models.IntegerField(default=0)
    enemy_max_ball_speed = models.IntegerField(default=0)
    max_exchange = models.IntegerField(default=0)
