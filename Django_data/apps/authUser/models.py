from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    idUser = models.AutoField(primary_key=True)
    status = models.BooleanField()
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=50, null=False)
    avatar = models.ImageField()

    USERNAME_FIELD = 'username'
