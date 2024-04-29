from django.shortcuts import HttpResponse, render
from django.views.generic import TemplateView

from apps.Game.models import Games, UserGame

import apps.Dashboard.tools as tools

import logging
logger = logging.getLogger(__name__)


class HistoryView(TemplateView):
    template_name = "histo.html"

    def get(self, request):
        parties = tools.party_played(request.user)
        opponents = tools.find_my_opponent(key=parties, me=request.user)
        ordered_party = tools.ordered_party(
            opponent_key=opponents, me=request.user
        )
        context = tools.data_constructor(ordered_party)
        for k, items in context.items():
            if items.get('id') is not None:
                logger.debug(f"{items.get('id').id = }")
        return render(request, self.template_name, {'context': context})

    def post(self, request):
        pass


class BoardView(TemplateView):
    template_name = "board.html"

    def get(self, request, _id: int):
        context = tools.party_sender(key=_id, me=request.user)
        return render(request, self.template_name, context=context)

    def post(self, request):
        pass
