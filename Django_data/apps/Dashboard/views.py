from django.shortcuts import render
from django.template import Template
from django.views.generic import TemplateView
from ..Game.models import Games, UserGame


class HistoryView(TemplateView):
    template_name = "histo.html"

    try:
        def get(self):
            pass

        def post(self):
            pass

    except Exception as exc:
        pass


class BoardView(TemplateView):
    pass
