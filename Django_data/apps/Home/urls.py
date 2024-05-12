from django.urls import path

from . import views

app_name = "apps.Home"

urlpatterns = [
  path("", views.home, name="home"),
	path("footer", views.footer, name="footer"),
	path("header", views.header, name="header"),
	path("404", views.error404, name="404"),
]