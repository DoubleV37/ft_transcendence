from django.shortcuts import HttpResponse, render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse

from apps.Game.models import Games, UserGame
from apps.Auth.models import User

import apps.Dashboard.tools as tools

import logging
logger = logging.getLogger(__name__)


class HistoryView(TemplateView):
    template_name = "Profile/GameHistory.html"

    def get(self, request, _id: int):
        target = User.objects.get(id=_id)
        parties = tools.party_played(target)
        opponents = tools.find_my_opponent(key=parties, me=target)
        ordered_party = tools.ordered_party(
            opponent_key=opponents, me=target
        )
        context = tools.data_constructor(ordered_party)
        for k, items in context.items():
            if items.get('id') is not None:
                logger.debug(f"{items.get('id').id = }")
        return render(request, self.template_name, {'context': context})

    def post(self, request):
        pass


class BoardView(TemplateView):
    template_name = "Game/Board.html"

    def get(self, request, _id: int):
        try:
            context = tools.party_sender(key=_id, me=request.user)
        except Exception as exc:
            return JsonResponse({'success': False, 'logs': 'Bad permission'})
        return render(request, self.template_name, context=context)

    def post(self, request):
        pass
