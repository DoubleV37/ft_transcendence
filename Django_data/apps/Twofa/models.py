from django.db import models
from django.conf import settings

class UserTwoFactor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='two_factor',
        on_delete=models.CASCADE
    )

    otp_secret = models.CharField(max_length=255)
