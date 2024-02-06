from django.urls import path

from . import views

app_name = "apps.website"
urlpatterns = [
    path("", views.home, name="home"),
	path("footer", views.footer, name="footer"),
	path("header", views.header, name="header"),
]
