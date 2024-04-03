from django.db import models
from django.conf import settings
from apps.Auth.models import User


class Friends1(models.Model):
    users1 = models.ManyToManyField(User, null=True)
    current_user = models.ForeignKey(
        User, related_name='owner', on_delete=models.CASCADE, null=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, create = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users1.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, create = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users1.remove(new_friend)


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        User, null=True, related_name='sender1', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
