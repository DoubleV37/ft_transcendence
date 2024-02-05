from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    status = models.BooleanField(default=True)
    username = models.CharField(primary_key=True, max_length=50, unique=True, null=False)
    email = models.CharField(max_length=50,unique=True, null=False)
    password = models.CharField(null=False)
    avatar = models.ImageField()

    USERNAME_FIELD = 'username'
