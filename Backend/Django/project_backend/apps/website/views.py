from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "index.html"

class UNView(TemplateView):
	template_name = "1.html"

class DEUXView(TemplateView):
	template_name = "2.html"

class TROISView(TemplateView):
	template_name = "3.html"

pages = [UNView, DEUXView, TROISView]

def section(request, num = 0):
	if num == 0:
		return IndexView.as_view()(request)
	elif 1 <= num <= 3:
		return pages[num-1].as_view()(request)
	else:
		raise Http404("No such section")
