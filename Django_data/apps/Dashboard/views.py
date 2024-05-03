from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse

from apps.Game.models import Games, UserGame
from apps.Auth.models import User

import apps.Dashboard.tools as tools
import apps.Dashboard.stat_fct as global_stats

import logging
logger = logging.getLogger(__name__)


class HistoryView(TemplateView):
    template_name = "Profile/GameHistory.html"

    def get(self, request, _id: int):
        target = User.objects.get(id=_id)
        parties = tools.party_played_by(target)
        opponents = tools.find_opponent(key=parties, me=target)
        ordered_party = tools.ordered_party(
            opponent_key=opponents, me=target
        )
        context = tools.populate_context(ordered_party)
        return render(request, self.template_name, {'context': context})


class BoardView(TemplateView):
    template_name = "Game/Board.html"

    def get(self, request, _id: int):
        try:
            context = tools.populate_dashboard(key=_id, me=request.user)
        except Exception as exc:
            return render(request, self.template_name, {'logs': 'error'})
        return render(request, self.template_name, context=context)


class GlobalStatsView(TemplateView):
    template_name = "gs.html"

    def get(self, request):
        context = global_stats.populate(key=request.user)
        return render(request, self.template_name, context=context)
