from django.shortcuts import HttpResponse, render
from django.views.generic import TemplateView

from apps.Game.models import Games, UserGame

import apps.Dashboard.tools as tools

import logging
logger = logging.getLogger(__name__)


class HistoryView(TemplateView):
    template_name = "histo.html"

    try:
        def get(self, request):
            parties = tools.party_played(request.user)
            opponents = tools.find_my_opponent(key=parties, me=request.user)
            ordered_party = tools.ordered_party(
                opponent_key=opponents, me=request.user
            )
            context = tools.dict_constructor(ordered_party)
            # logger.debug(f"{context = }")
            for key, values in context.items():
                logger.debug(f"{key = }")
                for v, value in values.items():
                    logger.debug(f"{value = }")
            return render(request, self.template_name, {'context': context})

        def post(self, request):
            pass

    except Exception as exc:
        pass


class BoardView(TemplateView):
    pass
