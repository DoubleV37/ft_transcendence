from django.forms import formset_factory
from django.shortcuts import redirect, render
from django.utils.translation.trans_real import receiver
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.generic.edit import Form
import apps.FriendsList.tools as tools
from apps.Auth.models import User
from apps.FriendsList.models import Friend_Request
from django.http import HttpResponse, JsonResponse

import logging
logger = logging.getLogger(__name__)


# def friend_request(request, pk):
#
#     sender = request.user
#     logger.info("")
#     logger.info(f"{' friend_request ':~^30}")
#     logger.info(f"{sender =}")
#
#     recipient = User.objects.get(id=pk)
#     logger.info(f"{recipient =}")
#
#     model = FriendRequest.objects.get_or_create(
#         sender=request.user, receiver=recipient)
#
#     return HttpResponse("<h1>OUAI</h1>")
#
#
# def delete_request(request, operation, pk):
#     client1 = User.objects.get(id=pk)
#     print(client1)
#     if operation == 'Sender_deleting':
#         model1 = FriendRequest.objects.get(
#             sender=request.user, receivers=client1)
#         model1.delete()
#     elif operation == 'Receiver_deleting':
#         model2 = FriendRequest.objects.get(
#             sender=client1, receivers=request.user)
#         model2.delete()
#         return redirect('/formation')
#
#     return redirect('/Display')
#
#


def add_or_remove_friend(request, operation, pk):
    new_friend = User.objects.get(id=pk)
    if operation == 'add':
        fq = FriendRequest.objects.get(
            sender=new_friend, receivers=request.user)
        Friends1.make_friend(request.user, new_friend)
        Friends1.make_friend(new_friend, request.user)
        fq.delete()
    elif operation == 'remove':
        Friends1.lose_friend(request.user, new_friend)
        Friends1.lose_friend(new_friend, request.user)
    return redirect('friends')


def send_friend_request(request, userID):
    from_user = request.user
    to_user = User.objects.get(id=userID)
    friend_request, created = Friend_Request.objects.get_or_create(
        from_user=from_user, to_user=to_user
    )
    if created:
        return HttpResponse('friend request sent')
    else:
        return HttpResponse('friend request alwready sent')


class FriendsRequestView(TemplateView):
    template_name = "FriendsList.html"

    try:

        def get(self, request):
            from_user = request.user
            myFriends = tools.myFriends(from_user)
            people = tools.UserDB(from_user)
            logger.info(f"{people = }")
            logger.info(f"{myFriends = }")
            return render(request, self.template_name,
                          {'from_user': from_user, 'people': people,
                              'myFriends': myFriends, }
                          )

        def post(self, request):
            logger.info("")
            logger.info(f"{' POST FUNCTION ':*^50}")
            logger.info(f"{ request.POST  = }")
            if request.method == 'POST':

                logger.info("")
                logger.info(f"{' INSIDE POST ':_^20}")
                logger.info(f"{ request.POST['add']  = }")

                target = User.objects.get(username=request.POST['add'])

                logger.info(f"{target = }")
                logger.info(f"{target.id = }")
                return send_friend_request(request, target.id)
            else:
                logger.info(f"in else method.POST way: ")

            return HttpResponse("Error")

    except Exception as exc:
        pass


def accept_or_refuse_FQ(request, data: list):
    logger.info(f"{' accept_or_refuse_FQ ':~^20}")
    logger.info(f"{data = }")
    friend_request = Friend_Request.objects.get(id=data[1])
    logger.info(f"{friend_request.to_user = }")
    logger.info(f"{request.user = }")
    if friend_request.to_user == request.user:
        if data[0] == 'add':
            friend_request.to_user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(friend_request.to_user)
            friend_request.delete()
            return HttpResponse('friend request accepted')
        elif data[0] == 'delete':
            friend_request.delete()
            return HttpResponse('friend request not accepted')
        else:
            return HttpResponse('Merde')
    else:
        return HttpResponse('Mierda')


class Accept_Or_Refuse_View(TemplateView):
    template_name = "RequestList.html"

    try:

        def get(self, request):
            me = request.user
            all_friend_request = Friend_Request.objects.all().filter(to_user=me)
            tmp = User.objects.all()

            for friend_request in all_friend_request:
                logger.info(f"{friend_request.to_user  = }")
            for user in tmp:
                logger.info(f"{user = }, {user.id = }")

            return render(
                request, self.template_name,
                {'me': me, 'all_friend_request': all_friend_request})

        def post(self, request):

            logger.info("")
            logger.info(f"{' INSIDE POST ':_^20}")
            logger.info(f"{ request.POST = }")
            logger.info(f"{ request.POST['key']  = }")

            result = str(request.POST['key'])
            tmpdata = list(result.split())
            target = User.objects.get(username=tmpdata[1])
            _user = request.user

            logger.info(f"{ target  = }")
            logger.info(f"{ _user  = }")

            tmpid = Friend_Request.objects.get(from_user=target, to_user=_user)

            logger.info(f"{ target.username  = }")
            logger.info(f"{ tmpid  = }")
            # logger.info(f"{ tmpid.to_user.id  = }")

            data = [tmpdata[0], tmpid.id]
            logger.info(f"{ data  = }")
            # return HttpResponse("<h1>OUAI</h1>")
            return accept_or_refuse_FQ(request, data)

    except Exception as exc:
        pass
