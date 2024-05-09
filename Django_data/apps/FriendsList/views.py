from django.shortcuts import render
from django.views.generic import TemplateView
import apps.FriendsList.tools as tools
from apps.Auth.models import User
from apps.FriendsList.models import Friend_Request
from django.http import JsonResponse, HttpResponse

import logging
logger = logging.getLogger(__name__)


class FriendsRequestView(TemplateView):
    template_name = "FriendList/FriendsList.html"

    try:

        def get(self, request):
            from_user = request.user
            myFriends = tools.myFriends(from_user)
            people = tools.suggestionList(from_user)
            all_friend_request = Friend_Request.objects.all().filter(to_user=from_user)
            return render(
                request, self.template_name,
                {'from_user': from_user, 'people': people, 'myFriends': myFriends, 'all_friend_request': all_friend_request}
            )

        def post(self, request):
            result = str(request.POST['key'])
            tmp = list(result.split())
            target = User.objects.get(username=tmp[1])

            if tmp[0].find("add") != -1:
                return tools.send_friend_request(request, target.id)

            elif tmp[0].find("delete") != -1:
                return tools.delete_friend(request, target)

            else:
                return JsonResponse(
                    {'success': False, 'logs': 'FriendRequestView error'}
                )

    except Exception as exc:
        pass


class Accept_Or_Refuse_View(TemplateView):
    template_name = "FriendList/RequestList.html"

    try:

        def get(self, request):
            me = request.user
            all_friend_request = Friend_Request.objects.all().filter(to_user=me)
            return render(
                request, self.template_name,
                {'me': me, 'all_friend_request': all_friend_request,})

        def post(self, request):
            result = str(request.POST['key'])
            tmp = list(result.split())
            target = User.objects.get(username=tmp[1])
            _user = request.user
            frid = Friend_Request.objects.get(from_user=target, to_user=_user)
            data = [tmp[0], frid.id]
            return tools.accept_or_refuse_FQ(request, data)

    except Exception as exc:
        pass


def friends_profile(request, _id=None):
    if _id is None or request.method != 'GET':
        return HttpResponse('Wrong Profile', status=400)
    my_user = request.user
    other_user = User.objects.get(id=_id)
    if other_user in my_user.friends.all():
        _type = 'delete'
    elif user_requested(my_user, other_user) is True:
        _type = 'request'
    else:
        _type = 'add'
    return render(request, 'Profile/Friends_Profile.html',
                  {'type': _type,
                   'username': other_user.username,
                   'id': other_user.id})


def user_requested(my_user, other_user):
    requested = {
        fr.from_user for fr in Friend_Request.objects.filter(to_user=my_user)
    }
    if other_user in requested:
        return True
    return False
