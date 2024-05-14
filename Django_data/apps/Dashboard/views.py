from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse

from apps.Game.models import Games, UserGame
from apps.Auth.models import User

import apps.Dashboard.tools as tools
import apps.Dashboard.stat_fct as global_stats

import logging
logger = logging.getLogger(__name__)


class HistoryView(TemplateView):
    template_name = "Profile/GameHistory.html"

    def get(self, request, _id: int):
      if "Load" not in request.headers:
        return redirect("/")
      target = User.objects.get(id=_id)
      parties = tools.party_played_by(target)
      logger.info(f"{parties = }")
      opponents = tools.find_opponent(key=parties, me=target)
      logger.info(f"{opponents = }")
      ordered_party = tools.ordered_party(
          opponent_key=opponents, me=target
      )
      logger.info(f"{ordered_party = }")
      context = tools.populate_context(ordered_party)
      return render(request, self.template_name, {'context': context})


class BoardView(TemplateView):
    template_name = "Game/Board.html"

    def get(self, request, _id: int):
        try:
            context = tools.populate_dashboard(key=_id, me=request.user)
        except Exception as exc:
            return redirect('404')
        return render(request, self.template_name, context=context)


class GlobalStatsView(TemplateView):
    template_name = "Game/Stats.html"

    def get(self, request, _id: int):
        try:
            target = User.objects.get(id=_id)
            context = global_stats.populate(key=target)
            return render(request, self.template_name, context=context)
        except Exception as exc:
            return redirect('404')


class ErrorView(TemplateView):
    template_error = "Errors/404.html"

    def get(self, request):
        return render(request, self.template_error)
