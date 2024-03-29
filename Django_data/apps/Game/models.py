from django.db import models

class MatchmakingUser(models.Model):
    channel_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.channel_name
