from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "home.html"

class HeaderView(TemplateView):
	template_name = "header.html"

class FooterView(TemplateView):
	template_name = "footer.html"

def header(request):
	return HeaderView.as_view()(request)

def footer(request):
	return FooterView.as_view()(request)

def home(request):
	return HomeView.as_view()(request)
