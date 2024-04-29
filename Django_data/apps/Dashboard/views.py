from django.shortcuts import render
from django.views.generic import TemplateView

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
        return render(request, self.template_name, {'context': context})


class BoardView(TemplateView):
    template_name = "board.html"

    def get(self, request, _id: int):
        try:
            context = tools.party_sender(key=_id, me=request.user)
        except Exception as exc:
            return render(request, self.template_name, {'logs': 'error'})
        return render(request, self.template_name, context=context)
