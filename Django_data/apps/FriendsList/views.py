from django.forms import formset_factory
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.generic.edit import Form
import apps.FriendsList.tools as tools
from apps.Auth.models import User
from .forms import FriendForm

import logging
logger = logging.getLogger(__name__)


class FriendsListView(TemplateView):
    template_name = "FriendsList.html"

    try:

        def get(self, request):
            me = request.user
            myFriends = tools.myFriends(me)
            toAdd = tools.UserDB(me)
            return render(
                request, self.template_name,
                {'me': me,
                 'toAdd': toAdd,
                 'myFriends': myFriends,
                 })

        def post(self, request):
            me = request.user
            toAdd = formset_factory(FriendForm)
            formset = FriendForm()
            if request.method == 'POST':
                formset = FriendForm(request.POST)
                if formset.is_valid():
                    key = formset
                    id = User.objects.all().filter(username=key)
                    me.friends.set(id)
                    me.save()
            return redirect("/")

    except Exception as exc:
        pass


def create_multiple_photos(request):
    PhotoFormSet = formset_factory(forms.PhotoForm, extra=5)
    formset = PhotoFormSet()
    if request.method == 'POST':
        formset = PhotoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    photo = form.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
            return redirect('home')
    return render(request, 'blog/create_multiple_photos.html', {'formset': formset})
