from django.db import models
from django.conf import settings
# Create your models here.


class FriendsList(models.Model):

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='from_user',
        on_delete=models.CASCADE
    )

    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='to_user',
        on_delete=models.CASCADE
    )
