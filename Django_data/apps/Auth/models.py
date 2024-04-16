from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db.models.fields import validators
from django.utils.text import slugify
from apps.Twofa.models import UserTwoFA
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
        max_length=13, validators=[MinLengthValidator(3)], unique=True, null=False)
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
        max_length=15, validators=[MinLengthValidator(3)],
        unique=True, null=False
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    # TODO function to manage size of avatar
    # def clean_image(self):
    #     image = self.avatar
    #     logger.debug(f"{image.width = }")
    #     if image:
    #         if image._size > 4*1024*1024/10000:
    #             raise ValidationError("Image file too large ( > 4mb )")
    #         return image
    #     else:
    #         raise ValidationError("Couldn't read uploaded image")

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.tournament_name:
            self.tournament_name = slugify(self) + "_t"
        super().save(*args, **kwargs)


@ receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        UserTwoFA.objects.create(user=instance)
    instance.to2fa.save()
