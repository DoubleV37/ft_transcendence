from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render
from apps.Auth.models import User

import logging
logger = logging.getLogger(__name__)


class FriendsListView(TemplateView):
    template_name = "FriendsList.html"

    try:

        def get(self, request):
            my_user = request.user
            toAdd = User.objects.all()
            return render(request, self.template_name, {'my_user': my_user, 'toAdd': toAdd})

    except Exception as exc:
        pass
