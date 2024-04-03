from django.forms import formset_factory
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.generic.edit import Form
import apps.FriendsList.tools as tools
from apps.Auth.models import User
from apps.FriendsList.models import FriendRequest, Friends1
from django.http import HttpResponse, JsonResponse

import logging
logger = logging.getLogger(__name__)


def friend_request(request, pk):

    sender = request.user
    logger.info("")
    logger.info(f"{' friend_request ':~^30}")
    logger.info(f"{sender =}")
    recipient = User.objects.get(id=pk)
    logger.info(f"{recipient =}")
    model = FriendRequest.objects.get_or_create(
        sender=request.user, receivers=recipient)

    return HttpResponse("<h1>OUAI</h1>")
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
# def add_or_remove_friend(request, operation, pk):
#     new_friend = User.objects.get(id=pk)
#     if operation == 'add':
#         fq = FriendRequest.objects.get(
#             sender=new_friend, receivers=request.user)
#         Friends1.make_friend(request.user, new_friend)
#         Friends1.make_friend(new_friend, request.user)
#         fq.delete()
#     elif operation == 'remove':
#         Friends1.lose_friend(request.user, new_friend)
#         Friends1.lose_friend(new_friend, request.user)
#     return redirect('form4')


class FriendsListView(TemplateView):
    template_name = "FriendsList.html"

    try:

        def get(self, request):
            me = request.user
            myFriends = tools.myFriends(me)
            toAdd = tools.UserDB(me)
            logger.info(f"{toAdd = }")
            logger.info(f"{myFriends = }")
            return render(
                request, self.template_name,
                {'me': me,
                 'toAdd': toAdd,
                 'myFriends': myFriends,
                 })

        def post(self, request):
            logger.info("")
            logger.info(f"{' POST FUNCTION ':*^50}")
            logger.info("")
            logger.info(f"{ request.POST  = }")
            me = request.user
            if request.method == 'POST':

                logger.info("")
                logger.info(f"{' INSIDE POST ':_^20}")
                logger.info("")
                logger.info("")
                logger.info(f"{ request.POST['add']  = }")
                target = User.objects.get(username=request.POST['add'])
                logger.info(f"{target = }")
                logger.info(f"{target.id = }")

                friend_request(request, target.id)
            # else:
            #         logger.info(f"in else .is_valid() way: {formset = }")
            else:
                logger.info(f"in else method.POST way: ")

            return redirect("/")

    except Exception as exc:
        pass


# def create_multiple_photos(request):
#     PhotoFormSet = formset_factory(forms.PhotoForm, extra=5)
#     formset = PhotoFormSet()
#     if request.method == 'POST':
#         formset = PhotoFormSet(request.POST, request.FILES)
#         if formset.is_valid():
#             for form in formset:
#                 if form.cleaned_data:
#                     photo = form.save(commit=False)
#                     photo.uploader = request.user
#                     photo.save()
#             return redirect('home')
#     return render(request, 'blog/create_multiple_photos.html', {'formset': formset})
