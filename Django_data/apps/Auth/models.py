from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.utils.text import slugify

class User(AbstractBaseUser):
    idUser = models.AutoField(auto_created = True, primary_key=True, unique=True, null=False)
    status = models.BooleanField(default=True)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    avatar = models.ImageField(default="default.png")

    tournament_name = models.CharField(max_length=50, unique=True, null=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username


    def save(self, *args, **kwargs):
        if not self.tournament_name:
            self.tournament_name = slugify(self) + "_tournament"
        super().save(*args, **kwargs)

