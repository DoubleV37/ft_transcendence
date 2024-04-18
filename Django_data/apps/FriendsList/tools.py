from apps.Auth.models import User
from django.http import JsonResponse
from apps.FriendsList.models import Friend_Request

import logging
logger = logging.getLogger(__name__)


def suggestionList(me: User) -> list:
    all_user = User.objects.all()
    friends = me.friends.all()
    requested = {
        fr.from_user for fr in Friend_Request.objects.filter(to_user=me)
    }
    lst = [
        item for item in all_user if item not in friends and item != me
        and item not in requested
    ]
    return lst


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
        return JsonResponse({'success': True, 'logs': 'Friend request sent'})
    else:
        return JsonResponse(
            {'success': True, 'logs': 'Request already send'}
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
