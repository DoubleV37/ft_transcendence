from apps.Auth.models import User
from django.http import JsonResponse
from apps.FriendsList.models import Friend_Request


def UserDB(me: User) -> list:
    toSort = User.objects.all()
    toRtrn = [user for user in toSort if user.username != me.username]
    return toRtrn


def myFriends(me: User) -> list:
    friends = [friend for friend in me.friends.all()]
    return friends


def delete_friend(request, target: User):
    request.user.friends.remove(target)
    target.friends.remove(request.user)
    return JsonResponse({'success': True, 'logs': 'friend removed'})


def send_friend_request(request, userID):
    from_user = request.user
    to_user = User.objects.get(id=userID)
    friend_request, created = Friend_Request.objects.get_or_create(
        from_user=from_user, to_user=to_user
    )
    if created:
        return JsonResponse({'success': True, 'logs': 'friend request sent'})
    else:
        return JsonResponse(
            {'success': True, 'logs': 'friend already request sent'}
        )


def accept_or_refuse_FQ(request, data: list):
    friend_request = Friend_Request.objects.get(id=data[1])
    if friend_request.to_user == request.user:
        if data[0] == 'add':
            friend_request.to_user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(friend_request.to_user)
            friend_request.delete()
            return JsonResponse(
                {'success': True, 'logs': 'friend request accepted'}
            )
        elif data[0] == 'delete':
            friend_request.delete()
            return JsonResponse(
                {'success': True, 'logs': "friend request didn't accept"}
            )
        else:
            return JsonResponse(
                {'success': False, 'logs': "Invalid button"}
            )
    else:
        return JsonResponse(
            {'success': False, 'logs': "Miss match target user"}
        )
