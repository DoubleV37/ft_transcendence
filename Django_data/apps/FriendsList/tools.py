from apps.Auth.models import User
from apps.FriendsList.models import FriendRequest


def UserDB(me: User) -> list:
    toSort = User.objects.all()
    toRtrn = [user for user in toSort if user.username != me.username]
    return toRtrn


def myFriends(me: User) -> list:
    friends = [friend for friend in me.friends.all()]
    return friends


# def filterFriendRequest(lst: list(FriendRequest), key: User) -> list:
#     return [obj for obj in lst if obj.receiver == key]
