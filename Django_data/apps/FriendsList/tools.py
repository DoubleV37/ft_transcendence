from apps.Auth.models import User
from .forms import FriendForm


def UserDB(me: User) -> list:
    toSort = User.objects.all()
    toRtrn = [FriendForm(instance=user)
              for user in toSort if user.username != me.username]
    return toRtrn


def myFriends(me: User) -> list:
    friends = [friend for friend in me.friends.all()]
    return friends
