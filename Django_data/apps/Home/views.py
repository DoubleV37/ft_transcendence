from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "Home/home.html"

class HeaderView(TemplateView):
	template_name = "Home/header.html"

class FooterView(TemplateView):
	template_name = "Home/footer.html"

def header(request):
	return HeaderView.as_view()(request)

def footer(request):
	return FooterView.as_view()(request)

def home(request):
	return HomeView.as_view()(request)
