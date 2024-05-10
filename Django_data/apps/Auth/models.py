from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db.models.fields import validators
from django.utils.text import slugify
from apps.Twofa.models import UserTwoFA
from apps.Dashboard.models import GlobalStats
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinLengthValidator
from .validators import validate_file_extension


import logging
logger = logging.getLogger(__name__)


class User(AbstractBaseUser):
    id = models.AutoField(
        auto_created=True, primary_key=True, unique=True, null=False)
    status = models.BooleanField(default=True)
    username = models.CharField(
        max_length=8, validators=[MinLengthValidator(3)], unique=True, null=False)
    email = models.EmailField(max_length=320, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)

    avatar = models.ImageField(
        default="ForbiddenDeletion/default.png", null=True, blank=True,
        validators=[validate_file_extension],
    )

    backup_avatar = models.ImageField(
        default="ForbiddenDeletion/default.png", null=False
    )

    refresh_token = models.CharField(max_length=255, null=True, blank=True)

    tournament_name = models.CharField(
        max_length=10, validators=[MinLengthValidator(3)],
        null=False
    )

    online_data = models.DateTimeField(default=timezone.now)
    in_game = models.BooleanField(default=False)

    skin_ball = models.CharField(
        default="/static/images/skins/ball/Ball_Cat.png", null=False)
    skin_paddle = models.CharField(
        default="/static/images/skins/paddle/Paddle_Grass.png", null=False)
    skin_background = models.CharField(
        default="/static/images/skins/background/BG_Forest.png", null=False)

    friends = models.ManyToManyField("self", blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    IMAGE_MAX_SIZE = (800, 800)

    objects = UserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.tournament_name:
            self.tournament_name = slugify(self) + "_t"
        super().save(*args, **kwargs)
        # TODO info back function to manage resize of avatar
        # self.resize_image()


@ receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        UserTwoFA.objects.create(user=instance)
        GlobalStats.objects.create(user=instance)
    instance.to2fa.save()
