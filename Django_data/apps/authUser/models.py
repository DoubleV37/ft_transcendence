from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    idUser = models.AutoField(primary_key=True, unique=True, null=False, default=1)
    status = models.BooleanField(default=True)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    avatar = models.ImageField(upload_to='avatars/')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

