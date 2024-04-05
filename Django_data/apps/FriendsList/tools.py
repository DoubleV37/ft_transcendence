from apps.Auth.models import User
from django.http import JsonResponse
from apps.FriendsList.models import Friend_Request

import logging
logger = logging.getLogger(__name__)

# def userDB(me: User) -> list(User):
#     toSort = User.objects.all()
#     toRtrn = [user for user in toSort if user.username != me.username]
#     return toRtrn


# TODO stopped here
# def buildlist(key: User, all_user: list, friends: lst) -> bool:
#     if key.


def suggestionList(me: User) -> list:
    lst = list()
    logger.info("")
    logger.info("suggestionList")
    logger.info(f"{me = }")
    all_user = User.objects.all()
    friends = me.friends.all()
    logger.info(f"{friends = }")
    for user in all_user:
        for friend in friends:
            if friend != user and
        try:
            logger.info(f"{user = }")
            test = friends.count(user)
            logger.info(f"{test = }")
            if test == 0:
                if user != me:
                    lst.append(user)
        except:
            logger.info(f"except: {user = }")
            if user != me:
                lst.append(user)

    # for person in friends:
    #     try:
    #
    #         if person != user:
    #             lst.index(user)
    #     except:
    #         if user != me:
    #             lst.append(user)
    #     # lst = [person for person in friends if user != person]
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
